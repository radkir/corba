# coding: utf-8
# flake8: noqa
"""
Client U2000.
"""
import managers
from data import me_names, equip_names, subnet_names

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def run_test(MgrCls, *args):
    m = MgrCls(*args)
    m.get_all_data()
    m.dump_data()


def ems_test():
    run_test(managers.Ems)

def equipment_inventory_test():
    run_test(managers.EquipmentInventory, me_names)

def managed_element_test():
    run_test(managers.ManagedElement)

def multilayer_subnetwork():
    run_test(managers.MultiLayerSubnetworkMgr, me_names, subnet_names)

def protection_test():
    run_test(managers.ProtectionMgr, me_names)

def hw_mstp_inventory_test():
    run_test(managers.HW_MSTPInventoryMgr, me_names, equip_names)

def hw_mstpprotectionmgr_test():
    run_test(managers.HW_MSTPProtectionMgr_I, me_names)

def trafficdescriptormgr_test():
    run_test(managers.TrafficDescriptorMgr_I, me_names)

def hw_controlplanemgr_test():
    run_test(managers.HW_controlPlaneMgr)

def encapsulationlayerlinkmgr_test():
    run_test(managers.EncapsulationLayerLinkMgr_I)

def flowdomainmgr_test():
    run_test(managers.FlowDomainMgr_I)

def maintenance_test():
    run_test(managers.MaintenanceMgr, me_names)

def tc_profile_mgr_test():
    run_test(managers.TCProfileMgr)

def trailntwprotmgr_test():
    run_test(managers.TrailNtwProtMgr_I, me_names)


if __name__ == '__main__':
    testst = list(x for x in globals() if x.endswith('_test'))
    failed = []
    for test in testst:
        try:
            globals()[test]()
        except Exception as ex:
            failed.append((test, ex))
        continue
    for f in failed:
        print(f)