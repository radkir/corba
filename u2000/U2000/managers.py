# coding: utf-8
# flake8: noqa
"""
Модуль CORBA менеджеров. 
"""
import os
from collections import namedtuple, OrderedDict, defaultdict
import json
import emsMgr
from managedElementManager import ManagedElementMgr_I
from equipment import EquipmentInventoryMgr_I
from template import _Mngr

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def _get_data(self):
    for req in self.requests.values():
        self.session = self.new_session()
        req.result.extend(self.call(req))


def _dump_data(self):
    for req in self.requests.values():
        json_file = f'{req.method}.json'
        req = [self.convert(x) for x in req.result]
        with open(json_file, 'w') as output:
            json.dump(req, output)


class Ems(_Mngr):

    def __init__(self):
        super().__init__()
        _reqs = ('getAllTopLevelSubnetworks', 'getAllTopLevelTopologicalLinks')
        for req in _reqs:
            self.requests[req] = self.make_request(req, 0)

    def get_data(self):
        _get_data(self)

    def dump_data(self):
        _dump_data(self)

    def get_manager(self):
        return self.session.getManager("EMS")


class ManagedElement(_Mngr):

    def __init__(self):
        super().__init__()
        _reqs = ('getAllManagedElements',)
        for req in _reqs:
            self.requests[req] = self.make_request(req, 0)

    def get_data(self):
        _get_data(self)

    def dump_data(self):
        _dump_data(self)

    def get_manager(self):
        return self.session.getManager("ManagedElement")._narrow(ManagedElementMgr_I)


class EquipmentInventory(_Mngr):

    def __init__(self, all_managed_element_names):
        super().__init__()
        self.all_managed_element_names = {str(x.name): x for x in all_managed_element_names}
        self.all_equipment = defaultdict(list)
        self.all_equipment_names = defaultdict(list)
        self.all_supported_ptps = defaultdict(list)
        self.all_supported_ptps_names = defaultdict(list)
        self.all_supporting_equipment = defaultdict(list)

        # связываем источник имен и куда будем выгружать результат
        Bind = namedtuple('Bind', ('source', 'destination'))
        self.requests = OrderedDict(
            {'getAllEquipment': Bind(self.all_managed_element_names, self.all_equipment),
             'getAllEquipmentNames': Bind(self.all_managed_element_names, self.all_equipment_names),
             'getAllSupportedPTPs': Bind(self.all_equipment_names, self.all_supported_ptps),
             'getAllSupportedPTPNames': Bind(self.all_equipment_names, self.all_supported_ptps_names),
             'getAllSupportingEquipment': Bind(self.all_supported_ptps_names, self.all_supporting_equipment)
             }
        )

    def get_manager(self):
        return self.session.getManager("EquipmentInventory")._narrow(EquipmentInventoryMgr_I)

    def get_data(self):
        for method, bind in self.requests.items():
            self.new_session()
            for name, obj in bind.source.items():
                req = self.make_request(method, obj, 0)
                result = self.call(req)
                if not isinstance(obj, str):
                    name = obj.name
                bind.destination[name].append(result)

    def dump_data(self):

        for meth, bind in self.requests.items():
            json_file = f'{meth}.json'
            for elem, req in bind.destination.items():
                req = self.convert(req)
            with open(json_file, 'w') as output:
                json.dump(bind.destination, output)
