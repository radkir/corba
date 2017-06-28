import emsSessionFactory
import nmsSession__POA
from omniORB import CORBA
import CosNaming

from settings import argv, login, pwd, NameComponents


class NmsSession_I(nmsSession__POA.NmsSession_I):
    pass


def Orb():
    """
    Initialise the ORB
    :return: 
    """
    orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
    if not orb:
        raise Exception("Failed ->CORBA.ORB_init(argv, CORBA.ORB_ID)")
    return orb


def root_naming_context(orb):
    """
    Obtain a reference to the root naming context
    :param orb: 
    :return: 
    """
    obj = orb.resolve_initial_references("NameService")
    rootContext = obj._narrow(CosNaming.NamingContext)
    if not rootContext:
        raise Exception("Failed ->narrow the root naming context")
    return rootContext


def resolve_the_name(rootContext, components):
    name = [CosNaming.NameComponent(*x) for x in components]
    try:
        obj = rootContext.resolve(name)
    except CosNaming.NamingContext.NotFound as ex:
        raise Exception(f"Except->Name not found. Info: {ex}")
    return obj


class Session(object):
    def __init__(self, root, login=login, pwd=pwd):
        self.__root = root
        self.__login = login
        self.__pwd = pwd
        self.__nms_session = None
        self.__ems_session = None

    root = property(fget=lambda self: self.__root, doc='rootContext object for narrow')

    @property
    def nms_session(self):
        if not self.__nms_session:
            nms_session_o = NmsSession_I()._this()
            if not nms_session_o:
                raise Exception("Object reference is not an NmsSession_I")
            self.__nms_session = nms_session_o
        return self.__nms_session

    @property
    def ems_session(self):
        if not self.__ems_session:
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
