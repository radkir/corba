import globaldefs
import emsMgr
from templates import Session, Orb, root_naming_context, resolve_the_name
from settings import NameComponents


def convert_param(args):
    for param in args:
        if isinstance(param, globaldefs.NameAndStringValue_T):
            param = {param.name: param.value}
        yield param


orb = Orb()
rootContext = root_naming_context(orb)
root = resolve_the_name(rootContext, NameComponents)
with Session(root) as session:
    ems_mng = session.ems_session.getManager("EMS")
    subnetw_list, subnetw_iter = ems_mng.getAllTopLevelSubnetworks(0)
    print(f'subnetw_list:{subnetw_list}')
    more = True
    while more:
        more, seq = subnetw_iter.next_n(1)
        for attr in seq:
            print('__')
            for key, value in attr.__dict__.items():
                if not isinstance(value, list):
                    value = [value]
                value = [x for x in convert_param(value)]
                print(f'param:{key};value:{value}')

    
    subnetw_list, subnetw_iter = ems_mng.getAllTopLevelTopologicalLinkNames(0)
    print(f'subnetw_list:{subnetw_list}')
    more = True
    while more:
        more, seq = subnetw_iter.next_n(1)
        for attr in seq:
            print('__')
            for key, value in attr.__dict__.items():
                if not isinstance(value, list):
                    value = [value]
                value = [x for x in convert_param(value)]
                print(f'param:{key};value:{value}')

