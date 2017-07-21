# coding: utf-8
# flake8: noqa
"""
Client U2000.
"""
from managers import Ems, ManagedElement, EquipmentInventory

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


if __name__ == '__main__':
    ems = Ems()
    ems.get_data()
    ems.dump_data()
