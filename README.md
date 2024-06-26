# Мотоциклы онлайн магазин


Этот проект - онлайн магазин мотоциклов, разработанный с использованием Django, DRF, PostgreSQL, Docker, Swagger etc.

## Описание

Проект включает в себя следующие основные функции:


- Отображение каталога мотоциклов с возможностью просмотра подробной информации о каждом мотоцикле.
- Добавление мотоциклов в корзину покупок и оформление заказа (только авторизированным пользователям).
- Возможность регистрации и аутентификации пользователей для управления своей корзиной.
- Так же у пользователей есть возможность добавлять собственные мотоциклы на продажу.
- Лента новостей и Sitemap 
- Кастомная админ-панель для приложения пользователей

## Установка 1 

1. Склонируйте репозиторий:
```
git clone https://github.com/Pony3n/Moto_sale.git
```
2. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Примените миграции:
```
python manage.py migrate
```
5. Поменяйте настройки для БД в файле setting.py:
```
        #'HOST': 'db',
         'HOST': '127.0.0.1',
```
6. Запустите сервер:
```
python manage.py runserver
```

## Установка 2 

1. Склонируйте репозиторий:
```
git clone https://github.com/Pony3n/Moto_sale.git
```
2. Находясь в директории проекта, активируйте команду:
```
docker compose up
```

## Использование

После запуска сервера вы сможете открыть приложение в вашем браузере по адресу [Moto seller](http://localhost:8000).

Если вы запускаете проект, используя Docker compose, то зайдите внутри контейнера с приложением:
```
docker exec -it <contained_ID> bash
```
И примените следующие команды:

Для автоматического создания супер-пользователя, введите команду:
```
python manage.py create_superuser
```
Информация о супер-пользователе находится moto_user -> management -> commands -> create_superuser

Так же, нужно вручную накатить миграции:
```
python manage.py migrate
```
Так же, чтобы вручную не создавать доп. пользователей, лоты мотоциклов и новости - 
используйте фикстуры приложений moto_user, motorcycles и moto_news:
```
python manage.py load_fixtures
```
## Автор

- Молодцов Андрей - разработчик программного кода - molodtsov_a_p@mail.ru
