# Treny New Fich

Небольшой сервис на FastAPI для работы с пользователями, товарами, фоновыми задачами, очередями и внешними API.

## Что есть в проекте

- `users` — регистрация, логин, получение текущего пользователя
- `products` — создание, обновление, удаление и чтение товаров
- `external_posts` — запросы к внешнему API постов
- `exchange_client` — конвертация валют
- `work_with_backtasks` — фоновые задачи
- RabbitMQ consumer/producer для асинхронной обработки событий

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy Async
- Alembic
- PostgreSQL
- RabbitMQ
- Pytest

## Структура проекта

- `main.py` — точка входа приложения
- `core/` — конфигурация, авторизация, модели и база данных
- `services/` — роуты, CRUD-логика и интеграции
- `utils/` — вспомогательные функции
- `tests/` — unit и integration тесты
- `docs/` — дополнительная документация

## Подготовка окружения

### 1. Установить зависимости

```bash
poetry install --no-root
```

### 2. Настроить `.env`

Пример значений:

```env
DB_URL=postgresql+asyncpg://app_user:app_password@localhost:5433/app_db
DB_ECHO=false
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5673
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### 3. Поднять инфраструктуру

```bash
docker compose up -d
```

### 4. Применить миграции

```bash
poetry run alembic upgrade head
```

## Запуск приложения

```bash
poetry run uvicorn main:app --reload
```

После запуска будут доступны:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Запуск тестов

Обычный запуск:

```bash
poetry run pytest
```

Покрытие:

```bash
poetry run coverage run -m pytest
poetry run coverage report -m
```

Цель по покрытию проекта: не ниже 80%.

## Полезные документы

- [Подход к тестированию](docs/testing_approach.md)
- [Документация по развертыванию](docs/deployment.md)
- [План инфраструктуры](docs/infrastructure_plan.md)

