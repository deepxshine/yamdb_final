![Yamdb Workflow Status](https://github.com/deepxshine/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)
# api_yamdb
api_yamdb

## Импорт данных из `csv` в БД
```
python manage.py importcsv
```

Параметры импорта задаются [здесь](https://github.com/suranovab/api_yamdb/blob/develop/api_yamdb/api_yamdb/management/commands/importcsv.py)


# API_YAMDB
REST API проект для сервиса YaMDb — сбор отзывов о фильмах, книгах или музыке.
## Описание 
Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
### Стек
Стек:
- Django 4.1.1
- DRF 3.14.0
- djangorestframework-simplejwt 5.2.1
- psycopg2-binary 2.9.3
- PyJWT 2.5.0
# Как запустить проект
Устанавливаем Docker и Docker-compose:
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Проверяем правильность установки Docker-compose:
```
sudo  docker-compose --version
```
Соберираем статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Применяем миграции:
```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
```
## Workflow
1) test - тестирование pep8 и pytest
2) push Docker image to Dockerhub - отправка образа в облако
3) deploy - отправка проекта на сервер
4) send message - отправка сообщения в телеграм
### GitHub Secrets 
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
TELEGRAM_TO - id чата в телеграме
TELEGRAM_TOKEN - токен телеграм бота

### Проект досупен по адресу
http://158.160.8.160/admin/login/?next=/admin/
### Автор проекта 
[Алексей Евдокимов](https://github.com/deepxshine)
