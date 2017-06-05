# coding: utf-8
import abc

from template import DockerObject
from tools import _input, _print


class Image(DockerObject):
    """DOCKER IMAGE"""

    @classmethod
    def info(cls, images=None):
        if not images:
            images = cls.__images()
        print('=' * 80)
        print('IMAGES:')
        for key, value in images.items():
            _print(f"[{key}]: {value}")
        print('=' * 80)

    @classmethod
    def remove(cls):
        """
        Remove docker images from input numbers or all temp images 
        ('REPOSITORY' == <none> and 'TAG' == <none>).
        These images could be created if build process was falled.
        """

        actions = {0: cls.all_images,
                   1: cls.none_images,
                   2: cls.custom_images
                   }

        while True:
            try:
                curent = cls.__images()
                cls.info(curent)
                print(f'Please, choise action for {cls.__doc__} [for exit: Ctr+C]:')
                print(f"[0] = remove ALL {cls.__doc__}'s info\n"
                      f"[1] = remove NONE {cls.__doc__}'s\n"
                      f"[2] = remove CUSTOM {cls.__doc__}'s"
                      )
                try:
                    answer = int(_input())
                    target_images = actions[answer](curent)
                    print('These images will be removed:')
                    print(target_images)
                    answer = input('Are you sure [yes/no]? For exit: [Ctr+C]').lower().strip()
                    if not answer == 'yes':
                        raise ValueError()
                    else:
                        for img_id in target_images:
                            res = call(f"docker rmi {img_id}")
                            _print(res.out)

                except KeyError:
                    raise ValueError()

            except ValueError as e:
                _print(f'Bad value. Please, repeat input...({e})')
                continue

            except KeyboardInterrupt:
                break

    @classmethod
    def __images(cls):
        return cls.manager.call('docker images')

    @classmethod
    def all_images(cls, images):
        return [x['IMAGE ID'] for x in images.values()]

    @classmethod
    def none_images(cls, images):
        none_images = []
        for id, data in images.items():
            marker = data['REPOSITORY'], data['TAG']
            if all(x == '<none>' for x in marker):
                none_images.append(data['IMAGE ID'])
        if not none_images:
            raise ValueError("Doesn't have NONE images.")
        return none_images

    @classmethod
    def custom_images(cls, images):
        _print(f'Please, input image numbers for delete [for exit: Ctr+C]:')
        id = [int(x) for x in _input().split()]
        if not all(i in images for i in id):
            raise ValueError("Bad image number")
        custom_images = [images.pop(i)['IMAGE ID'] for i in id]
        return custom_images