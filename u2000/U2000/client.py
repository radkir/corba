# coding: utf-8
# flake8: noqa
"""
Client U2000.
"""
from managers import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"



me_names = ([globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'), globaldefs.NameAndStringValue_T(name='ManagedElement', value='3145733')],
[globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'), globaldefs.NameAndStringValue_T(name='ManagedElement', value='3145736')],
[globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'), globaldefs.NameAndStringValue_T(name='ManagedElement', value='3145737')],
[globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'), globaldefs.NameAndStringValue_T(name='ManagedElement', value='3145738')],
[globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'), globaldefs.NameAndStringValue_T(name='ManagedElement', value='3145740')])


subnet_names = ([globaldefs.NameAndStringValue_T(name='EMS', value='Huawei/U2000RTN'),
               globaldefs.NameAndStringValue_T(name='MultiLayerSubnetwork', value='1')],
               )

def ems_test():
    ems = Ems()
    ems.get_all_data()
    ems.dump_data()

def managed_element_test():
    mem = ManagedElement()
    mem.get_all_data()
    mem.dump_data()

def equipment_inventory_test():
    eq = EquipmentInventory(me_names)
    eq.get_all_data()
    eq.dump_data()

def multilayer_subnetwork():
    mlayer = MultiLayerSubnetworkMgr(all_managed_element_names=me_names, subnet_names=subnet_names)
    mlayer.get_all_data()
    mlayer.dump_data()

def protection_test():
    pr = ProtectionMgr(me_names)
    pr.get_all_data()
    pr.dump_data()


if __name__ == '__main__':

    testst = (ems_test,
             managed_element_test,
             equipment_inventory_test,
             multilayer_subnetwork,
             protection_test,
             )

    for test in testst:
        try:
            test()
        except:
            print(f'Failed test {test.__name__}')
            continue