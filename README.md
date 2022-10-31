![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=badge&logo=nginx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=badge&logo=django&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-000000?.svg?style=ApacheKafka&logo=ApacheKafka)
![Celery](https://img.shields.io/badge/Celery-DBE4A?.svg?style=celery&logo=celery)

# Биллинг

Дипломный проект команды №1 16 когорты Яндекс.Практикума по направлению "Мидл Python разработчик"

# Состав команды

- [Остап](https://github.com/error1number404)
- [Эмир](https://github.com/Wiped-Out)
- [Александр](https://github.com/askalach)

# Описание сервиса

## Схема

<a href="https://imgbb.com/"><img src="https://i.ibb.co/HXH4Hj3/photo-2022-10-31-22-18-25.jpg" alt="photo-2022-10-31-22-18-25" border="0" /></a>

## Схема базы данных

<a href="https://ibb.co/Pg87mbp"><img src="https://i.ibb.co/JHPfBbL/photo-2022-10-31-22-35-42.jpg" alt="photo-2022-10-31-22-35-42" border="0" /></a>

## Как все работает

Авторизация пользователей в биллинг происходит через
наш [сервис авторизации](https://github.com/MiddlePython16/auth_service)

Если это администратор, то перекидываем его в админку, в которой можно изменять параметры подписок и следить за заказами

Если это пользователь, то перекидываем его на страницу оплаты подписки.

‼️ В качестве платежного сервиса мы выбрали ЮКассу, подключенную через библиотеку django-payments. Это позволяет нам
легко добавлять/менять/удалять провайдеров.

После оплаты в Celery передается задача на изменение прав у пользователя (теперь у него есть подписка, значит, он может
смотреть фильмы!). Эти права хранятся в базе данных биллинга. Но чтобы каждый раз не обращаться к базе за сверкой прав,
мы также добавляем их в access token, который генерирует [auth сервис](https://github.com/MiddlePython16/auth_service)

# Стек технологий

- Docker
- Python
- Django
- DRF
- Celery
- Postgres
- Kafka
- JWT

# Запуск

Для начала необходимо запустить [сервис авторизации](https://github.com/MiddlePython16/auth_service)

Затем запустите биллинг сервис. Для этого воспользуйтесь следующими командами

```
cd billing_compose
docker-compose up --build -d
```