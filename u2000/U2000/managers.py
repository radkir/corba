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
import protection, protection__POA

from template import _Mngr

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


# ------------------------------------------------------------------
class Ems(_Mngr):

    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllTopLevelSubnetworks',      # 0
                                          'getAllTopLevelTopologicalLinks'  # 1
                                          )
                       )
    name = property(fget=lambda self: "EMS",
                    doc='This interface is used to manage an EMS.'
                    )

    def set_bind(self):
        self.bind = {self.methods[0]: lambda: self.make_request(self.methods[0], True, 0),
                     self.methods[1]: lambda: self.make_request(self.methods[0], True, 0),
                     }


# ------------------------------------------------------------------
class ManagedElement(_Mngr):

    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllManagedElements',          # 0
                                          'getAllManagedElementNames'       # 1
                                          )
                       )
    name = property(fget=lambda self: "ManagedElement",
                    doc='This interface is used to manage NEs and termination points (TPs), '
                        'including NEs, ports, and cross-connections on NEs'
                    )

    def set_bind(self):
        self.bind = {self.methods[0]: lambda: self.make_request(self.methods[0], True, 0),
                     self.methods[1]: lambda: self.make_request(self.methods[1], True, 0)
                     }

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(ManagedElementMgr_I)


# ------------------------------------------------------------------
class EquipmentInventory(_Mngr):

    def __init__(self, all_managed_element_names=None):
        super().__init__()
        self.all_managed_element_names = all_managed_element_names

    methods = property(fget=lambda self: ('getAllEquipment',                # 0
                                          'getAllEquipmentNames',           # 1
                                          'getAllSupportedPTPNames',        # 2
                                          'getAllSupportingEquipment',      # 3
                                          'getAllEquipmentAdditionalInfo'   # 4
                                          )
                       )
    
    name = property(fget=lambda self: "EquipmentInventory",
                    doc='This interface is used to manage resources, '
                        'such as equipment, boards, and ports on boards'
                    )

    @property
    def long_equipment_names(self):
        for name in self.chain_request_result('getAllEquipmentNames'):
            if len(name) > 3:
                yield name

    def set_bind(self, *args, **kw):
        self.bind = {
            self.methods[0]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[0], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[1]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[1], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[2]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[2], True, name, 0),
                    self.long_equipment_names
                )
            ),
            self.methods[3]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[3], False, name),
                    self.chain_request_result('getAllSupportedPTPNames')
                )
            ),
            self.methods[4]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[4], False, name),
                    self.all_managed_element_names
                )
            ),
        }

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(EquipmentInventoryMgr_I)


# ------------------------------------------------------------------
class MultiLayerSubnetworkMgr(_Mngr):
    
    def __init__(self, me_names=None, subnet_names=None):
        super().__init__()
        self.all_managed_element_names = me_names
        self.subnet_names = subnet_names

    methods = property(fget=lambda self: ('getAllTopologicalLinks',         # 0
                                          'getAllInternalTopologicalLinks'  # 1
                                          )
                       )
    name = property(fget=lambda self: "MultiLayerSubnetwork",
                    doc='This interface is used to manage subnets.'
                    )

    def set_bind(self):
        self.bind = {
            self.methods[0]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[0], True, name, 0),
                    self.subnet_names
                )
            ),
            self.methods[1]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[1], True, name, 0),
                    self.all_managed_element_names
                )
            ),

        }


# ------------------------------------------------------------------
class ProtectionMgr(_Mngr):
    def __init__(self, me_names=None):
        super().__init__()
        self.all_managed_element_names = me_names

    methods = property(fget=lambda self: ('getAllProtectionGroups',         # 0
                                          'getAllWDMProtectionGroups',      # 1
                                          'getAllEProtectionGroups',        # 2
                                          'getAllIPProtectionGroups',       # 3
                                          'HW_getAllERPSProtectionGroups',  # 4
                                          'HW_getAllIFProtectionGroups',    # 5
                                          'HW_getAllXPICGroups',            # 6
                                          'getAllProtectionSubnetworks'     # 7
                                          )
                       )
    name = property(fget=lambda self: "Protection",
                    doc='This interface is used to manage protection groups.'
                    )

    def set_bind(self):
        self.bind = {
            self.methods[0]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[0], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[1]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[1], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[2]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[2], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[3]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[3], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[4]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[4], False, name),
                    self.all_managed_element_names
                )
            ),
            self.methods[5]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[5], False, name),
                    self.all_managed_element_names
                )
            ),
            self.methods[6]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[6], True, name, 0),
                    self.all_managed_element_names
                )
            ),
            self.methods[7]: lambda: tuple(
                map(
                    lambda name: self.make_request(self.methods[7], True, 0),
                    self.all_managed_element_names
                )
            ),
        }