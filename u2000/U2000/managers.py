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
from maintenanceOps import MaintenanceMgr_I
from trafficConditioningProfile import TCProfileMgr_I
from HW_mstpInventory import HW_MSTPInventoryMgr_I
from HW_controlPlane import HW_controlPlaneMgr_I
from trailNtwProtection import TrailNtwProtMgr_I
from encapsulationLayerLink import EncapsulationLayerLinkMgr_I

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
    name = property(fget=lambda self: 'EMS',
                    doc='This interface is used to manage an EMS.'
                    )

    def set_bind(self):
        for m in self.methods:
            self.bind[m] = lambda m=m: self.make_request(m, True, 0)


# ------------------------------------------------------------------
class EquipmentInventory(_Mngr):

    def __init__(self, me_names=None):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllEquipment',  # 0
                                          'getAllEquipmentNames',  # 1
                                          'getAllSupportedPTPNames',  # 2
                                          'getAllSupportedPTPs',  # 3
                                          'getAllSupportingEquipment',  # 4
                                          'getAllEquipmentAdditionalInfo'  # 5
                                          )
                       )

    name = property(fget=lambda self: 'EquipmentInventory',
                    doc='This interface is used to manage resources, '
                        'such as equipment, boards, and ports on boards'
                    )

    @property
    def long_equipment_names(self):
        for name in self.chain_request_result('getAllEquipmentNames'):
            if len(name) > 3:
                yield name

    def set_bind(self, *args, **kw):
        for i, m in enumerate(self.methods):
            names = self.all_managed_element_names
            if i < 4:
                if i in (2, 3):
                    names = self.long_equipment_names
                self.bind[m] = lambda names=names, m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, True, name, 0),
                        names
                        )
                )
            elif i in (4, 5):
                if i == 4:
                    names = self.chain_request_result('getAllSupportedPTPNames')
                self.bind[m] = lambda names=names, m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, False, name),
                        names
                        )
                )

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(EquipmentInventoryMgr_I)


# ------------------------------------------------------------------
class ManagedElement(_Mngr):

    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllManagedElements',          # 0
                                          'getAllManagedElementNames'       # 1

                                          )
                       )
    name = property(
        fget=lambda self: 'ManagedElement',
        doc='This interface is used to manage NEs and '
            'termination points (TPs), including NEs, '
            'ports, and cross-connections on NEs'
    )

    def set_bind(self):
        for m in self.methods:
            self.bind[m] = lambda m=m: self.make_request(m, True, 0)

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(ManagedElementMgr_I)


# ------------------------------------------------------------------
class MultiLayerSubnetworkMgr(_Mngr):
    
    def __init__(self, me_names=None, subnet_names=None):
        self.subnet_names = subnet_names
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllTopologicalLinks',         # 0
                                          'getAllManagedElements',          # 1
                                          'getAllInternalTopologicalLinks'  # 2
                                          )
                       )
    name = property(fget=lambda self: 'MultiLayerSubnetwork',
                    doc='This interface is used to manage subnets.'
                    )

    def set_bind(self):
        for i, m in enumerate(self.methods):
            names = self.all_managed_element_names
            if i < 2:
                names = self.subnet_names
            self.bind[m] = lambda names=names, m=m: tuple(
                map(lambda name, m=m: self.make_request(m, True, name, 0),
                    names
                    )
            )


# ------------------------------------------------------------------
class ProtectionMgr(_Mngr):
    def __init__(self, me_names=None):
        super().__init__(me_names)

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

    name = property(fget=lambda self: 'Protection',
                    doc='This interface is used to manage protection groups.'
                    )

    def set_bind(self):
        for i, m in enumerate(self.methods):
            if i in (0, 1, 2, 3, 6):
                self.bind[m] = lambda m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, True, name, 0),
                        self.all_managed_element_names
                        )
                )
            elif i in (4, 5):
                self.bind[m] = lambda m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, False, name),
                        self.all_managed_element_names
                        )
                )
            elif i in (7, ):
                self.bind[m] = lambda m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, True, 0),
                        self.all_managed_element_names
                        )
                )


# ------------------------------------------------------------------
class HW_MSTPInventoryMgr(_Mngr):
    def __init__(self, me_names=None, equip_names=None):
        self.equipment_names = equip_names
        super().__init__(me_names)

    methods = property(
        fget=lambda self: (
            'getAllVBs',                      # 0
            'getAllQosRules',                 # 1
            'getAllFlows',                    # 2
            'getAllLinkAggregationGroups',    # 3
            'getAllSpanningTrees',            # 4
            'getAllVLANs'                     # 5
        )
    )

    name = property(fget=lambda self: 'CORBA_MSTP_INV',
                    doc='This interface is used to manage MSTP inventories.'
                    )

    def set_bind(self):
        names = self.all_managed_element_names
        for i, m in enumerate(self.methods):
            if i == 4:
                names = self.equipment_names
            elif i == 5:
                names = self.chain_request_result('getAllVBs')
            self.bind[m] = lambda names=names, m=m: tuple(
                map(lambda name, m=m: self.make_request(m, True, name, 0),
                    names
                    )
            )

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(HW_MSTPInventoryMgr_I)


# ------------------------------------------------------------------
class HW_MSTPProtectionMgr_I(_Mngr):
    def __init__(self, me_names):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllRPRNode',
                                          'getAllAtmProtectGroup',
                                          'getAllRPRLinkInfo'
                                          )
                       )

    name = property(fget=lambda self: 'CORBA_MSTP_PRO',
                    doc="""This interface is used to manage the MSTP protection."""
                    )

    def set_bind(self):
        for m in self.methods:
            self.bind[m] = lambda m=m: tuple(
                map(lambda name, m=m: self.make_request(m, True, name, 0),
                    self.all_managed_element_names
                    )
            )

# ------------------------------------------------------------------
class HW_MSTPServiceMgr_I(_Mngr):
    def __init__(self, me_names):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllETHService',
                                          'getAllATMService',
                                          )
                       )

    name = property(fget=lambda self: 'CORBA_MSTP_SVC',
                    doc="""This interface is used to manage MSTP services."""
                    )


# ------------------------------------------------------------------
class TrafficDescriptorMgr_I(_Mngr):
    def __init__(self, me_names):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('HW_getAllTrafficDescriptors',))

    name = property(fget=lambda self: 'CORBA_MSTP_TD',
                    doc="""This interface is used to manage traffic
                     descriptors and supported in only the MSTP equipment."""
                    )

    def set_bind(self):
        m = self.methods[0]
        self.bind[m] = lambda m=m: tuple(
            map(lambda name, m=m: self.make_request(m, True, name, 0),
                self.all_managed_element_names
                )
        )


# ------------------------------------------------------------------
class HW_controlPlaneMgr(_Mngr):
    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllRoutingAreaNames',
                                          'getAllRoutingNodeNames',
                                          'getAllSnppLinks'
                                          )
                       )

    name = property(fget=lambda self: 'ControlPlane',
                    doc="""This interface is used to query details of all 
                    SNPP links in a routing area according to routing area name."""
                    )

    def set_bind(self):
        for i, m in enumerate(self.methods):
            if i == 0:
                self.bind[m] = lambda m=m: self.make_request(m, False)
            elif i == 1:
                self.bind[m] = lambda m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, True, name, 0),
                        (x for x in self.chain_request_result('getAllRoutingAreaNames'))
                        )
                )
            elif i == 2:
                self.bind[m] = lambda m=m: tuple(
                    map(lambda name, m=m: self.make_request(m, True, name, 0),
                        (x for x in self.chain_request_result('getAllRoutingNodeNames'))
                        )
                )

    def set_manager(self):
        super().set_manager()
        self.mgr = self.mgr._narrow(HW_controlPlaneMgr_I)


# ------------------------------------------------------------------
class EncapsulationLayerLinkMgr_I(_Mngr):
    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllELLinks',))

    name = property(fget=lambda self: 'ELLManagement',
                    doc="""This interface is used to query information 
                    about encapsulation layer links (ELLs)."""
                    )

    def set_bind(self):
        m = self.methods[0]
        self.bind[m] = lambda m=m: self.make_request(m, True, 0)


# ------------------------------------------------------------------
class FlowDomainMgr_I(_Mngr):

    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('getAllFlowDomains',))

    name = property(fget=lambda self: 'FlowdomainManagement',
                    doc="""This interface is used to query information 
                    about flow domain fragments and matrix flow domain
                    fragments. The MSTP equipment is supported only."""
                    )

    def set_bind(self):
        m = self.methods[0]
        self.bind[m] = lambda m=m: self.make_request(m, True, 0)

# ------------------------------------------------------------------
class MaintenanceMgr(_Mngr):
    def __init__(self, me_names=None):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllMaintenanceDomains',
                                          'getAllMaintenanceAssociations',
                                          'getAllMaintenancePoints'
                                          )
                       )

    name = property(fget=lambda self: 'Maintenance',
                    doc='This interface is used to manage maintenance functions.'
                    )

    @property
    def all_md_names(self):
        for x in self.chain_request_result('getAllMaintenanceDomains'):
            yield x.name

    def set_bind(self):
        names = self.all_managed_element_names
        for i, m in enumerate(self.methods):
            if i > 0:
                names = self.all_md_names
            self.bind[m] = lambda names=names, m=m: tuple(
                map(lambda name, m=m: self.make_request(m, True, name, 0),
                    names
                    )
            )


# ------------------------------------------------------------------
class TCProfileMgr(_Mngr):
    def __init__(self):
        super().__init__()

    methods = property(fget=lambda self: ('HW_getAllTCProfiles',))

    name = property(
        fget=lambda self: 'TrafficConditioningProfile',
        doc="""This interface is used to manage traffic policy profiles. 
        Traffic policy profiles include port, Ethernet V-UNI ingress or egress,
        PW, ATM, ATM COS mapping and DS domain mapping policy profiles. 
        PTN equipment is supported"""
    )

    def set_bind(self):
        m = self.methods[0]
        self.bind[m] = lambda m=m: self.make_request(m, True, 0)


# ------------------------------------------------------------------
class  HW_VPNMgr_I(_Mngr):
    pass


# ------------------------------------------------------------------
class TrailNtwProtMgr_I(_Mngr):

    def __init__(self, me_names=None):
        super().__init__(me_names)

    methods = property(fget=lambda self: ('getAllTrailNtwProtections', ))

    name = property(fget=lambda self: 'TrailNetworkProtection',
                    doc="""This interface provides protection for network trails, including tunnels."""
                    )

    def set_bind(self):
        m = self.methods[0]
        self.bind[m] = lambda m=m: tuple(
            map(lambda name, m=m: self.make_request(m, True, name, 0),
                self.all_managed_element_names
                )
        )
