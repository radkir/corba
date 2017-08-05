# coding: utf-8
# flake8: noqa
"""
Модуль CORBA шаблонов. 
"""
import abc
import os
from collections import namedtuple, defaultdict
from itertools import chain

from omniORB import CORBA
import CosNaming
import emsSessionFactory
import globaldefs
import nmsSession, nmsSession__POA

from settings import argv, login, pwd, NameComponents, data_folder

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class NmsSession_I(nmsSession__POA.NmsSession_I):
    pass


class _Session(object):
    """
    Class of interface CORBA-session. Has context manager interface.
    """

    def __init__(self, login, pwd):
        self.__login = login
        self.__pwd = pwd
        self.__root = None
        self.__nms_session = None
        self.__ems_session = None

        self.orb_init()

    login = property(fget=lambda self: self.__login, doc='login')
    pwd = property(fget=lambda self: self.__pwd, doc='login of user U2000')
    root = property(fget=lambda self: self.__root, doc='password of user U2000')

    def orb_init(self):
        """
        CORBA.ORB_init, then resolve NameService with CosNaming.NamingContext.
        """
        orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
        if orb is None:
            raise Exception("Failed ->CORBA.ORB_init(argv, CORBA.ORB_ID)")

        # Obtain a reference to the root naming context
        obj = orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)
        if rootContext is None:
            raise Exception("Failed ->narrow the root naming context")

        # Resolve the name
        name = [CosNaming.NameComponent(*x) for x in NameComponents]

        try:
            self.__root = rootContext.resolve(name)
        except CosNaming.NamingContext.NotFound as ex:
            raise Exception(f"Except->Name not found.\nInfo: {ex}")

    @property
    def nms_session(self):
        """
        Resolve NmsSession_I.
        
        :return: NmsSession
        """
        nms_session_o = NmsSession_I()._this()
        if not nms_session_o:
            self.close()
            raise Exception("Object reference is not an NmsSession_I")
        self.__nms_session = nms_session_o
        return self.__nms_session

    @property
    def ems_session(self):
        """
        Resolve EmsSessionFactory_I.

        :return: EmsSession
        """
        session = self.root._narrow(emsSessionFactory.EmsSessionFactory_I)
        if not session:
            self.close()
            raise Exception("Object reference is not an EmsSessionFactory_I")
        self.__ems_session = session.getEmsSession(self.__login, self.__pwd, self.nms_session)
        return self.__ems_session

    def get_manager(self, name):
        """
        Return manager from  EmsSessionFactory_I.
        
        :param name: manager name
        """
        try:
            self.close()
            self.orb_init()
            return self.ems_session.getManager(name)
        except Exception as e:
            self.close()
            raise Exception(e)

    def get_supported_managers(self):
        """
        CORBA_MSTP_INV
        CORBA_MSTP_PRO
        CORBA_MSTP_SVC
        CORBA_MSTP_TD
        CORBA_VPN
        ControlPlane
        ELLManagement
        EMS
        EquipmentInventory
        FlowdomainManagement
        GuiCutThrough
        Maintenance
        ManagedElement
        MultiLayerSubnetwork
        PerformanceManagement
        Protection
        SecurityManagement
        TopoManagement
        TrafficConditioningProfile
        TrailNetworkProtection
        """
        return self.ems_session.getSupportedManagers()

    def close(self):
        if self.ems_session:
            self.ems_session.endSession()
            self.__nms_session = self.__ems_session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.__login = self.__pwd = None


class _Mngr(metaclass=abc.ABCMeta):
    """
    Class of interface CORBA NBI.
    """
    __Request = namedtuple('Request', ('method', 'complex', 'params', 'result'))

    def __init__(self, all_managed_element_names=None, *args):
        self.session = _Session(login, pwd)
        self.mgr = None
        self.set_manager()

        self.requests = defaultdict(list)
        # TODO: Этот здесь лишнее -
        # TODO: вынести логику name, methods в конструктор
        self.all_managed_element_names = all_managed_element_names
        self.bind = {}
        self.set_bind()

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def methods(self):
        pass

    @abc.abstractmethod
    def set_bind(self):
        """
        Метод устанавливает связку метода и исходных данных, 
        которые ему будут передаваться.
        """
        pass

    def set_manager(self):
        if self.name not in self.session.get_supported_managers():
            raise TypeError('This kind of manager is not supported in current broker')
        self.mgr = self.session.get_manager(self.name)

    # --------------------- Request  -----------------
    def make_request(self, method, complex, *params):
        r = self.__Request(method, complex, params, [])
        self.requests[method].append(r)

    def make_multilayer_requests(self):
        if not self.requests:
            requests = lambda: defaultdict(requests)
            self.requests = requests()

    def chain_request_result(self, method):
        return chain(*(x.result for x in self.requests[method]))

    @staticmethod
    def make_holder_name(self, name, value):
        return globaldefs.NameAndStringValue_T(name=name, value=value)

    # --------------------- Get data methods ---------
    def get_all_data(self):
        for meth in self.methods:
            self.bind[meth]()
            try:
                self.get_data(meth)
            except Exception as ex:
                print(f'\n\nGet data exception.'
                      f'\nManager={self.name}, method={meth}.'
                      f'\nException: {ex}\n\n'
                      )
            continue

    def get_data(self, method):
        if not self.requests[method]:
            raise Exception('Empty requests')
        for req in self.requests[method]:
            self.call(req)

    def call(self, request):
        """
        Call of manager for get data.

        :param request: 
        :param complex: if it's True when return 2 objects: list, _objref_Iterator_I
        """
        try:
            self.set_manager()
            if not self.mgr:
                raise Exception(f'{self.name} Manager have not created!')

            method = getattr(self.mgr, request.method)
            res = method(*request.params)
            if request.complex:
                _list, _iter = res
                res = tuple(self.iterator(_iter))
            else:
                if not isinstance(res, (list, tuple)):
                    res = (res,)
            if request.result:
                print(f'Clear old result of method={request.method}')
                request.result = []
            request.result.extend(res)
        finally:
            self.session.close()

    def iterator(self, iter_T):
        if not iter_T:
            print('Empty iterator!')
            return
        more = True
        while more:
            try:
                more, seq = iter_T.next_n(1)
                for attr in seq:
                    yield attr
            except Exception as e:
                print(f'Iteration Error: {e}')
                raise StopIteration()

    # --------------------- Dump data methods ---------
    def dump_data(self):
        path = self.make_data_folder()
        for method, requests in self.requests.items():
            file = os.path.join(path, f'{method}.dat')
            with open(file, 'w') as out:
                for req in requests:
                    for x in req.result:
                        out.write(f'{x}\n')
                    out.write('\n')
            self.requests[method] = []

    def make_data_folder(self):
        folder_name = f'{self.name.lower()}_data'
        path = os.path.join(data_folder, folder_name)
        os.makedirs(path, exist_ok=True)
        return path

    def convert(self, arg):
        """
        Converting data from CORBA-type to json-serialize.

        :param arg: json-serialized arg
        """
        if isinstance(arg, list):
            return [self.convert(x) for x in arg]
        elif type(arg).__module__ != 'builtins':
            return tuple((key, self.convert(value)) for key, value in arg.__dict__.items())
        else:
            return arg
