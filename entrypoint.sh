#!/bin/bash

echo "Ожидание подключения к базе данных и применение миграций..."

# Функция для применения миграций с повторными попытками
run_migrations() {
    max_retries=30
    retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        echo "Попытка применения миграций... ($((retry_count + 1))/$max_retries)"
        
        if alembic upgrade head; then
            echo "Миграции успешно применены"
            return 0
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                echo "Ожидание подключения к БД... (через 2 секунды повторим попытку)"
                sleep 2
            fi
        fi
    done
    
    echo "Не удалось применить миграции после $max_retries попыток"
    exit 1
}

# Применяем миграции
run_migrations

echo "Запуск приложения..."

# Запускаем приложение
exec "$@"

