from collections import namedtuple

addr = '172.23.25.72:12001'
login = 'corbanbi2'
pwd = 'Corbanbi_2'

argv = ["-ORBInitRef", f"NameService=corbaloc::{addr}/NameService"]

NameComponents = (
    ("TMF_MTNM", "Class"),
    ("HUAWEI", "Vendor"),
    ("Huawei/U2000RTN", "EmsInstance"),
    ("2.0", "Version"),
    ("Huawei/U2000RTN", "EmsSessionFactory_I")
)
