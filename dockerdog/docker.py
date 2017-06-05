# coding: utf-8

import subprocess as sp
from collections import namedtuple

from tools import convert, _input, _print
from image import Image
from containers import Container


class DockerDog(object):

    @staticmethod
    @convert
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
        result.err = map(decode, err)
        result.out = map(decode, out)
        return result

    @classmethod
    def main(cls):

        objects = {0: Image, 1: Container}
        actions = {0: 'info', 1: 'create', 2: 'remove'}

        while True:
            try:
                print('Please, choise object [for exit: Ctr+C]:')
                print('[0] = IMAGE\n[1] = CONTAINER (unactive)')
                obj = objects[int(_input())]

                while True:
                    print(f'Please, choise action for __{obj.__doc__}__ [for exit: Ctr+C]:')
                    print(f'[0] = info\n'
                          f'[1] = create (unactive)\n'
                          f'[2] = remove'
                          )
                    try:
                        action = getattr(obj, actions[int(_input())])
                        action()
                    except (KeyError, KeyboardInterrupt, TypeError):
                        raise ValueError()

            except ValueError as e:
                _print(f'Bad value. Please, repeat input...{e}')
                continue

            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    Image.set_manager(DockerDog)
    Container.set_manager(DockerDog)
    DockerDog.main()
