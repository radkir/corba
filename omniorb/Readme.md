
Создание образа производится в каталоге с Dockerfile:
	$docker build --rm -t vladworldss/omniorb .

Запуск контейнера:
	$docker run -it --name omniorb vladworldss/omniorb

Запуск контейнера c монтированием директории хоста:
        $docker run -it --volume /tmp/omniorb:/omniorb --name omniorb vladworldss/omniorb

Удаление всех завершившихся контейнеров
	$docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
