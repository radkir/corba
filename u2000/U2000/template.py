# coding: utf-8
# flake8: noqa
"""
Модуль CORBA шаблонов. 
"""

from collections import namedtuple, defaultdict

from omniORB import CORBA
import CosNaming
import emsSessionFactory
import globaldefs
import nmsSession, nmsSession__POA

from settings import argv, login, pwd, NameComponents

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class NmsSession_I(nmsSession__POA.NmsSession_I):
    pass


class _Session(object):
    """
    Класс CORBA-сессии. Поддерживает интерфейс контекстного менеджера.
    """
    def __init__(self, login=login, pwd=pwd):
        self.__login = login
        self.__pwd = pwd
        self.__root = None
        self.__nms_session = None
        self.__ems_session = None

        # Initialise the ORB
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

    root = property(fget=lambda self: self.__root, doc='rootContext object for narrow')

    @property
    def nms_session(self):
        nms_session_o = NmsSession_I()._this()
        if not nms_session_o:
            raise Exception("Object reference is not an NmsSession_I")
        self.__nms_session = nms_session_o
        return self.__nms_session

    @property
    def ems_session(self):
        session = self.root._narrow(emsSessionFactory.EmsSessionFactory_I)
        if not session:
            raise Exception("Object reference is not an EmsSessionFactory_I")
        self.__ems_session = session.getEmsSession(self.__login, self.__pwd, self.nms_session)
        return self.__ems_session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ems_session.endSession()
        self.__root = self.__login = self.__pwd = self.__nms_session = self.__ems_session = None


class _Mngr(object):
    """
    Обертка над интерфейсом Mgr_I
    """

    __Request = namedtuple('Request', ('method', 'params', 'result'))

    def __init__(self):

        self.session = None
        self.mgr = None
        self.new_session()
        requests = lambda: defaultdict(requests)
        self.requests = requests()

    def call(self, request):
        if not self.mgr:
            raise Exception('EMS manager have not created!')
        method = getattr(self.mgr, request.method)
        _list, _iter = method(*request.params)
        result = tuple((x for x in self.iterator(_iter)))
        return result

    def convert(self, arg):
        """
        Метод преобразования corba-типов в json-serialize.
        :param arg: 
        :return: 
        """
        if isinstance(arg, list):
            return [self.convert(x) for x in arg]
        elif type(arg).__module__ != 'builtins':
            return tuple((key, self.convert(value)) for key, value in arg.__dict__.items())
        else:
            return arg

    def dump_data(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def get_manager(self):
        raise NotImplementedError

    def new_session(self):
        self.session = _Session().ems_session
        self.mgr = self.get_manager()

    def holder_name(self, name, value):
        return globaldefs.NameAndStringValue_T(name=name,value=value)

    def iterator(self, iter_T):
        if not iter_T:
            assert 'None iterator!'
            return
        more = True
        while more:
            more, seq = iter_T.next_n(1)
            for attr in seq:
                yield attr

    def make_request(self, method, *params):
        return self.__Request(method, params, [])
