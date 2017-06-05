# coding: utf-8
import abc


class DockerObject(metaclass=abc.ABCMeta):
    """Base class for docker objects"""

    manager = None

    @classmethod
    def set_manager(cls, mgr):
        cls.manager = mgr

    @abc.abstractclassmethod
    def info(cls): pass

    @abc.abstractclassmethod
    def create(cls): pass

    @abc.abstractclassmethod
    def remove(cls, *args): pass


class DockerError(Exception):
    """
    Класс исключений Docker
    """
