# coding: utf-8
from collections import OrderedDict
import pprint
from functools import wraps


def _print(obj):
    """Print wrapper for prettyprint"""
    pp = pprint.pformat(obj, indent=1, width=150, depth=None)
    print(pp)


def _input(*args, **kw):
    """Strip input values"""
    return input(*args, **kw).strip()


def convert(foo):
    """Deco for convert stdout, stderr to OrderedDict"""
    @wraps(foo)
    def wrapper(*args, **kw):
        """
        Decorator for converting result from docker_daemon into dict like as
        {key=int: {key=table_name: value=data}}

        >>>
        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        ioss/omniorb        latest              b3410d90e98b        5 days ago          871 MB

        >>>
        {1: {'REPOSITORY':'ioss/omniorb', 'TAG': 'latest', 'IMAGE ID': 'b3410d90e98b' ...}

        :param res: namedtuple('result', ['err', 'out'])
        :return: dict({int: {table_name: data}})

        """
        res = foo(*args, **kw)
        out = (x.split('  ') for x in res.out)
        skip = lambda li: tuple(filter(lambda x: x != '', li))
        out = [row for row in map(skip, out)]
        table_names = [x.strip() for x in out.pop(0)]
        result = OrderedDict()
        for i, data in enumerate(out):
            result[i] = dict(zip(table_names, (x.strip() for x in data)))
        return result
    return wrapper
