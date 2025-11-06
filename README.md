# Incidents API

REST API для управления инцидентами, реализованное на FastAPI с использованием Domain Driven Design архитектуры.

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** (async) - ORM для работы с базой данных
- **asyncpg** - асинхронный драйвер для PostgreSQL
- **Alembic** - инструмент для миграций базы данных
- **Pydantic** - валидация данных
- **Python 3.12** - версия Python

## Структура проекта

```
app/
├── core/              # Общие настройки (БД, конфигурация)
│   ├── config.py     # Настройки приложения
│   └── database.py   # Подключение к БД
├── incidents/         # Доменная область инцидентов
│   ├── model.py      # SQLAlchemy модели
│   ├── schema.py     # Pydantic схемы
│   ├── service.py    # Бизнес-логика
│   ├── repository.py # Работа с БД
│   ├── router.py     # FastAPI роутеры
│   └── dependencies.py # Dependency injection
└── main.py           # Точка входа приложения
```

## Требования

- Python 3.12 или выше
- PostgreSQL 15 или выше
- Docker и Docker Compose (для запуска через Docker)

## Установка и запуск

### Вариант 1: Запуск через Docker (рекомендуется)

Самый простой способ запустить приложение - использовать Docker Compose. Все настройки (включая автоматические миграции) уже настроены.

#### Шаг 1: Проверка установки Docker

Убедитесь, что Docker и Docker Compose установлены:

```bash
docker --version
docker-compose --version
```

#### Шаг 2: Клонирование и переход в директорию проекта

```bash
cd incidents-api
```

#### Шаг 3: Настройка переменных окружения (опционально)

Создайте файл `.env` в корне проекта (если его нет):

```bash
# Windows PowerShell
New-Item -ItemType File -Path .env

# Linux/Mac
touch .env
```

Добавьте в файл `.env` следующие переменные (или оставьте значения по умолчанию):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=incidents_db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/incidents_db
API_PORT=8000
DEBUG=false
```

#### Шаг 4: Запуск приложения

```bash
docker-compose up --build
```

При первом запуске это может занять несколько минут, так как будут скачаны образы и установлены зависимости.

Приложение автоматически:
- Создаст и запустит PostgreSQL базу данных
- Применит все миграции при старте (через `entrypoint.sh`)
- Запустит API сервер

#### Шаг 5: Проверка работоспособности

После запуска вы увидите в логах сообщения о готовности. Откройте в браузере:

- **API**: http://localhost:8000
- **Документация Swagger**: http://localhost:8000/docs
- **Альтернативная документация ReDoc**: http://localhost:8000/redoc

#### Остановка приложения

```bash
# Остановка с сохранением данных
docker-compose stop

# Остановка и удаление контейнеров (данные БД сохраняются в volumes)
docker-compose down

# Остановка с удалением всех данных (включая БД)
docker-compose down -v
```

#### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api

# Только база данных
docker-compose logs -f db
```

### Вариант 2: Локальная установка (без Docker)

#### Шаг 1: Установка Python

Убедитесь, что установлен Python 3.12 или выше:

```bash
python --version
# или
python3 --version
```

#### Шаг 2: Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Шаг 3: Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Шаг 4: Установка и настройка PostgreSQL

Убедитесь, что PostgreSQL установлен и запущен:

```bash
# Проверка статуса (Linux/Mac)
sudo systemctl status postgresql

# Windows: проверьте через Services или pgAdmin
```

Создайте базу данных:

```bash
# Подключитесь к PostgreSQL
psql -U postgres

# Создайте базу данных
CREATE DATABASE incidents_db;

# Выйдите
\q
```

#### Шаг 5: Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db
DEBUG=false
```

Или установите переменные окружения напрямую:

**Windows PowerShell:**
```powershell
$env:DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db"
$env:DEBUG="false"
```

**Windows CMD:**
```cmd
set DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db
set DEBUG=false
```

**Linux/Mac:**
```bash
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db"
export DEBUG=false
```

#### Шаг 6: Применение миграций

```bash
alembic upgrade head
```

Если миграции применены успешно, вы увидите сообщение:
```
INFO  [alembic.runtime.migration] Running upgrade -> accf7da576c7, initial
```

#### Шаг 7: Запуск приложения

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Флаг `--reload` включает автоматическую перезагрузку при изменении кода (только для разработки).

#### Шаг 8: Проверка работоспособности

Откройте в браузере:
- **API**: http://localhost:8000
- **Документация**: http://localhost:8000/docs

## Тестирование API

### Использование Swagger UI

Самый простой способ протестировать API - использовать встроенную документацию Swagger:
1. Откройте http://localhost:8000/docs
2. Выберите эндпоинт
3. Нажмите "Try it out"
4. Заполните параметры и нажмите "Execute"

### Использование curl

#### 1. Создать инцидент

```bash
curl -X POST "http://localhost:8000/incidents/" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Проблема с сервером",
    "source": "monitoring"
  }'
```

#### 2. Получить список инцидентов

```bash
# Все инциденты
curl -X GET "http://localhost:8000/incidents/"

# С фильтром по статусу
curl -X GET "http://localhost:8000/incidents/?status=open"
```

#### 3. Обновить статус инцидента

```bash
curl -X PATCH "http://localhost:8000/incidents/1/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### Использование PowerShell (Windows)

#### 1. Создать инцидент

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/incidents/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"description": "Проблема с сервером", "source": "monitoring"}'
```

#### 2. Получить список инцидентов

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/incidents/"
```

## Эндпоинты API

### 1. Создать инцидент
**POST** `/incidents/`

**Тело запроса:**
```json
{
  "description": "Проблема с сервером",
  "source": "monitoring"
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "description": "Проблема с сервером",
  "source": "monitoring",
  "status": "open",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. Получить список инцидентов
**GET** `/incidents/`

**Query параметры:**
- `status` (опционально) - фильтр по статусу: `open`, `in_progress`, `resolved`, `closed`

**Примеры:**
- `GET /incidents/` - все инциденты
- `GET /incidents/?status=open` - только открытые инциденты

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "description": "Проблема с сервером",
    "source": "monitoring",
    "status": "open",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### 3. Обновить статус инцидента
**PATCH** `/incidents/{incident_id}/status`

**Параметры пути:**
- `incident_id` (integer) - ID инцидента

**Тело запроса:**
```json
{
  "status": "in_progress"
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "description": "Проблема с сервером",
  "source": "monitoring",
  "status": "in_progress",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Ошибки:**
- `404 Not Found` - инцидент с указанным ID не найден

## Модель данных

Инцидент содержит следующие поля:

- `id` (integer) - уникальный идентификатор (автоматически генерируется)
- `description` (string, 1-5000 символов) - описание инцидента
- `status` (enum) - статус инцидента:
  - `open` - открыт (по умолчанию при создании)
  - `in_progress` - в работе
  - `resolved` - решен
  - `closed` - закрыт
- `source` (enum) - источник инцидента:
  - `operator` - оператор
  - `monitoring` - система мониторинга
  - `partner` - партнер
- `created_at` (datetime) - время создания (автоматически устанавливается)

## Переменные окружения

Все настройки управляются через переменные окружения (используется Pydantic Settings):

### Для Docker Compose

- `POSTGRES_USER` - пользователь PostgreSQL (по умолчанию: `postgres`)
- `POSTGRES_PASSWORD` - пароль PostgreSQL (по умолчанию: `postgres`)
- `POSTGRES_DB` - имя базы данных (по умолчанию: `incidents_db`)
- `POSTGRES_PORT` - порт PostgreSQL (по умолчанию: `5432`)
- `API_PORT` - порт API сервера (по умолчанию: `8000`)
- `DEBUG` - режим отладки (по умолчанию: `false`)

### Для локального запуска

- `DATABASE_URL` - полный URL подключения к базе данных (по умолчанию: `postgresql+asyncpg://postgres:postgres@localhost:5432/incidents_db`)
- `DEBUG` - режим отладки (по умолчанию: `false`)

Переменные можно задать через файл `.env` в корне проекта или через переменные окружения системы.

## Миграции базы данных

### Автоматические миграции (Docker)

При запуске приложения через Docker автоматически применяются все миграции Alembic через shell скрипт `entrypoint.sh`. Скрипт:
- Ожидает готовности базы данных (до 30 попыток с интервалом 2 секунды)
- Применяет все миграции через команду `alembic upgrade head`
- Запускает приложение только после успешного применения миграций

Если миграции уже применены, Alembic автоматически пропустит их.

### Ручное управление миграциями

#### Создание новой миграции

```bash
alembic revision --autogenerate -m "описание изменений"
```

#### Применение миграций

```bash
# Применить все миграции
alembic upgrade head

# Применить до конкретной версии
alembic upgrade <revision>

# Откатить последнюю миграцию
alembic downgrade -1

# Откатить все миграции
alembic downgrade base
```

#### Просмотр текущей версии

```bash
alembic current
```

#### Просмотр истории миграций

```bash
alembic history
```

## Решение проблем

### Проблема: Порт уже занят

**Ошибка:** `Address already in use` или `Port 8000 is already in use`

**Решение:**
- Измените порт в `.env` файле: `API_PORT=8001`
- Или остановите процесс, использующий порт:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # Linux/Mac
  lsof -ti:8000 | xargs kill -9
  ```

### Проблема: Не удается подключиться к базе данных

**Ошибка:** `Connection refused` или `Could not connect to database`

**Решение:**
1. Убедитесь, что PostgreSQL запущен
2. Проверьте правильность `DATABASE_URL` в `.env`
3. Проверьте, что порт PostgreSQL не занят другим процессом
4. Для Docker: убедитесь, что контейнер БД запущен: `docker-compose ps`

### Проблема: Миграции не применяются

**Ошибка:** `Target database is not up to date`

**Решение:**
```bash
# Применить все миграции вручную
alembic upgrade head

# Если проблема сохраняется, проверьте логи
docker-compose logs api
```

### Проблема: Модуль не найден

**Ошибка:** `ModuleNotFoundError: No module named 'app'`

**Решение:**
1. Убедитесь, что виртуальное окружение активировано
2. Убедитесь, что все зависимости установлены: `pip install -r requirements.txt`
3. Запускайте из корневой директории проекта

### Проблема: Permission denied для entrypoint.sh

**Ошибка:** `Permission denied` (Linux/Mac)

**Решение:**
```bash
chmod +x entrypoint.sh
```

## Разработка

### Структура кода

Проект следует принципам Domain Driven Design:

- **Models** (`app/incidents/model.py`) - SQLAlchemy модели для работы с БД
- **Schemas** (`app/incidents/schema.py`) - Pydantic схемы для валидации входных/выходных данных
- **Repositories** (`app/incidents/repository.py`) - слой доступа к данным
- **Services** (`app/incidents/service.py`) - бизнес-логика
- **Routers** (`app/incidents/router.py`) - HTTP эндпоинты
- **Dependencies** (`app/incidents/dependencies.py`) - dependency injection для FastAPI

### Добавление нового эндпоинта

1. Добавьте метод в `repository.py` (если нужна работа с БД)
2. Добавьте метод в `service.py` (бизнес-логика)
3. Добавьте схему в `schema.py` (если нужна новая валидация)
4. Добавьте роут в `router.py`
5. Создайте миграцию, если изменили модель: `alembic revision --autogenerate -m "описание"`

