В каталоге oracle-instantclient12.2 должны лежать:
	oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
	oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
	oracle-instantclient12.2-jdbc-12.2.0.1.0-1.x86_64.rpm
	oracle-instantclient12.2-odbc-12.2.0.1.0-1.x86_64.rpm
	oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm
	oracle-instantclient12.2-tools-12.2.0.1.0-1.x86_64.rpm

Создание образа производится в каталоге с Dockerfile:
	$docker build --rm -t ioss/oracleclient .

Запуск контейнера:
	$docker run -it --name oracleclient ioss/oracleclient

Удаление всех завершившихся контейнеров
	$docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
