Создание образа производится в каталоге с Dockerfile:
	$docker build --rm -t vladworldss/u2000 .

Сжатие образа
        $docker save vladworldss/u2000 | bzip2 > u2000.bz2

Копирование образа на сервер
        $scp u2000.bz2 dspars@172.28.5.36://home/dspars/corba

Распаковка образа
        $sudo docker load < u2000.bz2

Запуск контейнера:
	$docker run -it --name omniorb vladworldss/u2000

Запуск контейнера c монтированием директории хоста:
        $docker run -it --volume /home/dspars/corba:/corba --name u2000 vladworldss/u2000

Удаление всех завершившихся контейнеров
	$docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
