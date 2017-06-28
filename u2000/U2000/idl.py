# coding: utf-8
import os
import shutil
from collections import namedtuple
import pprint
import subprocess as sp


class CompileError(Exception):
    pass


def _print(obj):
    """Print wrapper for prettyprint"""
    pp = pprint.pformat(obj, indent=1, width=150, depth=None)
    print(pp)


def _input(*args, **kw):
    """Strip input values"""
    return input(*args, **kw).strip()


def call(cmd, terminal='/bin/bash'):
    """
    Exec command into terminal.

    :param cmd: command string
    :param terminal: path to terminal
    :return: namedtuple('result', ['err', 'out'])
    """
    result = namedtuple('result', ['err', 'out'])
    with sp.Popen(cmd, shell=True, executable=terminal, stdout=sp.PIPE, stderr=sp.PIPE) as pipe:
        err = pipe.stderr.readlines()
        out = pipe.stdout.readlines()
    decode = lambda x: x.decode('utf-8').strip()
    result.err = tuple(map(decode, err))
    result.out = tuple(map(decode, out))
    return result


def idl_listdir(path=None):
    if not path:
        path = os.getcwd()
    listdir = (x for x in os.listdir(path) if x.endswith('.idl'))
    return listdir


def copy_idl(dir_from, dir_to):
    """
    
    :param dir_from: 
    :param dir_to: 
    :return: 
    """
    for idl in idl_listdir(dir_from):
        path = f'{dir_from}/{idl}'
        shutil.copy(path, dir_to)
        print(f'copied file={path}')


def compile(name, preprocessor_path=None):
    """
    Метод компиляции idl с помощью omniidl в *.py модули.
    Скомпилированные файлы и пакеты с зависимостями будут распологаться в текущем каталоге.
    
    :param name: имя idl-файла
    :param preprocessor_path: путь для препроцессора, где лежат компилируемые idl
    :return: 
    """
    if not preprocessor_path:
        cmd= f'omniidl -bpython -I . {name}'    
    else:
        cmd= f'omniidl -bpython -I {preprocessor_path} {preprocessor_path}/{name}' 
    
    res = call(cmd)
    if res.err:
        print(res.err)
        raise CompileError()


def all_compile(path=None):
    """
    Компилиция всех idl-файлов.
    
    :param path: путь директории, где находятся idl; 
    :return: список нескомпилированных idl.
    """
    bad_idl = []
    for idl in idl_listdir(path):
        try:
            compile(idl, path)
        except CompileError:
            bad_idl.append(idl)
    print(f"Compiling are finished. Uncompile idl's: {bad_idl}")
    return bad_idl


if __name__ == '__main__':
    base_dir = '/root/corba/omniORB'
    dir_from = f'{base_dir}/omniORB_install/share/idl/omniORB/'
    dir_to = f'{base_dir}/idl'
    u2000_dir = f'{base_dir}/U2000'

    if not os.path.exists(u2000_dir):
        os.mkdir(u2000_dir)
    os.chdir(u2000_dir)
    copy_idl(dir_from, dir_to)
    all_compile(dir_to)
