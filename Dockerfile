FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Копирование и настройка entrypoint скрипта
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Порт приложения
EXPOSE 8000

# Используем entrypoint для запуска миграций перед приложением
ENTRYPOINT ["/entrypoint.sh"]

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

