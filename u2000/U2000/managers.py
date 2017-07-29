# coding: utf-8
# flake8: noqa
"""
Модуль CORBA менеджеров. 
"""
import os
from collections import namedtuple, OrderedDict, defaultdict
import json

import emsMgr
from equipment import EquipmentInventoryMgr_I
import globaldefs
from managedElementManager import ManagedElementMgr_I
from multiLayerSubnetwork import MultiLayerSubnetworkMgr_I

from template import _Mngr

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class Ems(_Mngr):

    _methods = ('getAllTopLevelSubnetworks', 'getAllTopLevelTopologicalLinks')

    def __init__(self):
        super().__init__()
        for meth in self._methods:
            self.make_request(meth, True, 0)

    name = property(fget=lambda self: "EMS", doc='This interface is used to manage an EMS.')


class ManagedElement(_Mngr):

    _methods = ('getAllManagedElements',)

    def __init__(self):
        super().__init__()
        for meth in self._methods:
            self.make_request(meth, True, 0)

    name = property(fget=lambda self: "ManagedElement",
                    doc='This interface is used to manage NEs and termination points (TPs), '
                        'including NEs, ports, and cross-connections on NEs'
                    )

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(ManagedElementMgr_I)


class EquipmentInventory(_Mngr):


    def __init__(self, all_managed_element_names=None):
        super().__init__()
        self.all_managed_element_names = all_managed_element_names

    name = property(fget=lambda self: "EquipmentInventory",
                    doc='This interface is used to manage resources, such as equipment, '
                        'boards, and ports on boards'
                    )

    def getAllEquipment(self, end=None):
        m = 'getAllEquipment'
        for me_name in self.all_managed_element_names[:end]:
            self.make_request(m, True, me_name, 0)
        self.get_data(m)

    def getAllEquipmentNames(self, end=None):
        m = 'getAllEquipmentNames'
        for me_name in self.all_managed_element_names[:end]:
            self.make_request(m, True, me_name, 0)
        self.get_data(m)

    def getAllSupportedPTPNames(self, end=None):
        m = 'getAllSupportedPTPNames'
        for req in self.requests['getAllEquipmentNames'][:end]:
            long_eq_names = (x for x in req.result if len(x)>3)
            for name in long_eq_names:
                self.make_request(m, True, name, 0)
        self.get_data(m)

    def getAllSupportingEquipment(self, end=None):
        m = 'getAllSupportingEquipment'
        for req in self.requests['getAllSupportedPTPNames'][:end]:
            for name in req.result:
                self.make_request(m, False, name)
        self.get_data(m)

    def getAllEquipmentAdditionalInfo(self, end=None):
        m = 'getAllEquipmentAdditionalInfo'
        for name in self.all_managed_element_names[:end]:
            self.make_request(m, False, name)
        self.get_data(m)

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(EquipmentInventoryMgr_I)
