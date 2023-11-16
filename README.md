# Foodgram

## Используемые технологии

[![foodgram_workflow](https://github.com/SerdgioTheCreator/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](https://github.com/SerdgioTheCreator/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Описание
Foodgram - сервис для публикации рецептов. 
 
Данный сервис поможет всегда иметь под рукой рецепты любимых блюд и формировать список покупок для упрощения похода в магазин за ингредиентами. 
Понятный и приятный глазу интерфейс позволит с легкостью погрузиться в мир кулинарии.
 
Авторизованные пользователи Foodgram смогут:
- публиковать свои рецепты 
- добавлять в избранное свои и чужие рецепты
- фильтровать рецепты по тегам
- добавлять рецепты в список покупок
- скачивать список покупок в формате .pdf
- подписываться на пользователей

## Подготовка и запуск проекта

### Шаблон для наполнения .env файла:

```
SECRET_KEY=<секретный ключ проекта Django>
DB_ENGINE=<django.db.backends.postgresql> #для PostgreSQL
или
DB_ENGINE=<django.db.backends.sqlite3> #для Sqlite3
ALLOWED_HOSTS=<строка с вашими хостами через запятую>
DEBUG=<False>
DB=<True> #для PostgreSQL
или
DB=<False> #для Sqlite3
DB_NAME=<наименование БД>
POSTGRES_USER=<пользователь БД>
POSTGRES_PASSWORD=<пароль для пользователя БД>
DB_HOST=db 
DB_PORT=5432 
```

- Клонировать репозиторий:

```
git clone https://github.com/SerdgioTheCreator/foodgram-project-react
```
- Выполнить вход на удаленный сервер
- Установить docker на сервер:

```
sudo apt install docker.io 
```
- Установить docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- Локально отредактировать файл infra/nginx.conf, обязательно в строке server_name вписать IP-адрес сервера
- Создать дирректорию foodgram/ и скопировать в нее папку docs:

```
mkdir foodgram
scp -r docs <username>@<host>:/home/<username>/foodgram/
```
- Создать дирректорию infra/ внутри дирректории foodgram/
- Скопировать файлы docker-compose.yml и nginx.conf из локальной директории infra/ в дирректорию infra/ на сервер:

на сервере:
```
cd foodgram
```

```
mkdir infra
```
на локальной машине:
```
scp docker-compose.yml <username>@<host>:/home/<username>/foodgram/infra/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/foodgram/infra/nginx.conf
```

- Создать и отредактировать.env файл в дирректории infra/ по предлагаемому выше шаблону.

```
touch .env
nano .env
```

- Для работы с Workflow добавить в Secrets GitHub переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql #для PostgreSQL
или
DB_ENGINE=django.db.backends.sqlite3 #для Sqlite3
ALLOWED_HOSTS=<строка с вашими хостами через запятую>
DEBUG=False
DB=True #для PostgreSQL
или
DB=False #для Sqlite3
DB_NAME=<наименование БД>
POSTGRES_USER=<пользователь БД>
POSTGRES_PASSWORD=<пароль для пользователя БД>
DB_HOST=db 
DB_PORT=5432 

DOCKER_USERNAME=<имя пользователя DockerHub>    
DOCKER_PASSWORD=<пароль от DockerHub>
    
SECRET_KEY=<секретный ключ проекта Django>
USER=<username для подключения к серверу>
HOST=<IP адрес сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
TELEGRAM_TO=<ID телеграм-аккаунта, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
Workflow состоит из четырёх шагов:
1. Проверка кода на соответствие PEP8 
2. Сборка и публикация образа бекенда и фронтенда на DockerHub. 
3. Автоматический деплой на удаленный сервер. 
4. Отправка уведомления в телеграм-чат.

- собрать и запустить контейнеры на сервере:
```
sudo docker-compose up -d
```

- После успешной сборки выполнить следующие действия:

Выполнить миграции:

```
sudo docker exec backend python3 manage.py makemigrations
sudo docker exec backend python3 manage.py migrate
```

Собрать статику:

```
sudo docker exec backend python3 manage.py collectstatic
```

Загрузить предустановленный список ингредиентов и тегов:

```
sudo docker exec backend python3 manage.py load_data_json
```

Создать суперюзера Django:

```
sudo docker exec -it backend python3 manage.py createsuperuser
```

- Ссылка на развернутый в облаке проект:

[http://bestfoodgram.ddns.net](https://bestfoodgram.ddns.net)

### Примеры API-запросов
Подробные примеры запросов и коды ответов приведены в прилагаемой
документации в формате ReDoc по адресу:


[http://bestfoodgram.ddns.net/api/docs/](https://bestfoodgram.ddns.net/api/docs/)


## Авторы: Коновалов Сергей, команда ЯндексПрактикум 