# Twitter Clone Backend

**Корпоративный сервис микроблогов**. Реализован на FastAPI + PostgreSQL.

## Функционал

Создание/удаление твитов  
Система подписок (follow/unfollow)  
Лайки твитов  
Загрузка медиафайлов в твиты  
**Лента** по популярности от фолловингов  
Профили пользователей (`/api/users/me`, `/api/users/{id}`)

## Технический стек

| Компонент | Технология | Версия |
|-----------|------------|--------|
| Backend | FastAPI | 0.115.0 |
| ASGI | Uvicorn | 0.30.6 |
| **Database** | **PostgreSQL** | **15-alpine** |
| ORM | SQLAlchemy | 2.0.35 |
| Мигр. | Alembic | 1.13.2 |
| Тесты | pytest | 8.3.2 |
| Линтинг | Ruff | 0.6.2 |

## Запуск

### Предварительные требования
- Docker и Docker Compose

### 1. Клонировать и запустить
```bash
git clone <repository-url>
cd twitter-backend
cp .env.example .env
docker-compose up -d