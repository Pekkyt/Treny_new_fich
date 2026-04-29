# Развертывание

## Что нужно для запуска

- Python 3.13
- Poetry
- Docker и Docker Compose
- PostgreSQL
- RabbitMQ

На практике PostgreSQL и RabbitMQ удобно поднимать через `docker compose`.

## Переменные окружения

Приложение использует такие переменные:

- `DB_URL`
- `DB_ECHO`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `RABBITMQ_HOST`
- `RABBITMQ_PORT`
- `RABBITMQ_USER`
- `RABBITMQ_PASSWORD`

## Локальное развертывание

### 1. Установить зависимости

```bash
poetry install --no-root
```

### 2. Поднять PostgreSQL и RabbitMQ

```bash
docker compose up -d
```

По текущей конфигурации будут открыты:

- PostgreSQL: `localhost:5433`
- RabbitMQ AMQP: `localhost:5673`
- RabbitMQ UI: `http://localhost:15673`

### 3. Применить миграции

```bash
poetry run alembic upgrade head
```

### 4. Запустить API

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Развертывание на сервере

Рекомендуемый порядок:

1. Склонировать репозиторий
2. Заполнить `.env`
3. Установить зависимости через Poetry
4. Поднять PostgreSQL и RabbitMQ
5. Выполнить миграции
6. Запустить приложение
7. Проверить `/docs` и базовые health-сценарии

## Что проверить после запуска

- приложение отвечает на HTTP-запросы
- авторизация работает
- подключение к базе данных успешно
- RabbitMQ доступен
- создание товара не ломает отправку задач в очередь

## CI/CD

В репозитории уже есть GitHub Actions:

- `.github/workflows/ci.yml` — линтинг и базовые тесты
- `.github/workflows/ci-cd.yml` — type check, lint, tests with coverage и шаг деплоя

## Что стоит улучшить дальше

- добавить Dockerfile в основную документацию деплоя
- добавить отдельный healthcheck endpoint
- вынести секреты в менеджер секретов, а не хранить только в `.env`
- добавить reverse proxy и TLS для production

