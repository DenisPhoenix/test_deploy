# Указываем базовый образ
FROM python:3.14-slim

# Устанавливаем переменные окружения для Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Обновить список доступных пакетоа и установить зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry без сохранения кэша pip
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения и без dev-пакетов
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта в контейнер
COPY .. /app

# Создает директории для медии в контейнере
RUN mkdir /app/media

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]