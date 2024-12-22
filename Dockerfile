# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Копируем весь код проекта в контейнер
COPY . /app/

# Устанавливаем Gunicorn для продакшн-режима
RUN pip install gunicorn

# Запускаем приложение с помощью Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

