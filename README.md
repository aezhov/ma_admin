Example Django project for currencies model
===========================================

Пример простой Django-админки и модели валют


* Free software: MIT license

Для удобства завёрнута в docker-compose вместе с Postgres.


Запуск
------

Проверка, что всё в порядке (код, тесты, внутренние чеки):

```bash
make check
```

Собственно, запуск сервиса:

```bash
make begin
```

Админка будет доступна по _http://localhost:8000/admin/_

Суперюзера можно создать так:

```bash
make superuser
```
   
Собственно валюты можно загрузить либо кнопкой в админке, либо, например, через management-команду `load_currencies`, то есть так:

```bash
make cli
./manage.py load_currencies 
```

Полная очистка:


```bash
make begin
```
   
Зависимости
-----------

Для управления зависимостями используется `pipenv`. Соответственно, посмотреть требуемые для проекта пакеты можно в файле `Pipfile`.
