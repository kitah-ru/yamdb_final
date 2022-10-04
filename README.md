# **YaMDB**
[![Python](https://img.shields.io/badge/Python-3.7.9-lightgreen?logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-2.2.19-lightgreen?logo=Django)](https://www.djangoproject.com/)
[![django-rest-framework](https://img.shields.io/badge/DRF-3.12.4-lightgreen?logo=DRF)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## **Описание:**
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории и жанры с возможностью поиска по определенным критериям. Пользователи могут оставлять к произведениям отзывы и ставить им оценку, таким образом, из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

---

### В данном проекте реализованы:
- Архитектура REST API (DRF);
- Разграничение доступа пользователей на основе permissions;
- Авторизация при помощи JWT токенов;
- Фильтрация данных на основе GET запросов;
- Сериализация и валидация данных (в том числе создание собственного поля);
- Получение в целях безопасности переменных окружения из файла .env;
- Контейнеризация Docker и Docker Compose с разворачиванием проекта при помощи Nginx, Gunicorn, PostgresQL;
- CI/CD с использованием GitHub Workflow.

---

### Как запустить проект:
1. Клонировать репозиторий и перейти в каталог с файлом композиции:
```
git clone git@github.com:kitah-ru/infra_sp2.git | cd infra_sp2/infra/
```

2. Запустить docker-compose:
```
docker-compose up -d --build
```

Примеры запросов к API можно посмотреть по адресу /redoc/ после запуска проекта.

---

### **Автор:**
[Никита Наталенко](https://github.com/kitahkitah/)

















