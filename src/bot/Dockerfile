# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app/src

# Копируем общий requirements (если есть) или локальный для bot
COPY requirements.txt /bot/app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /bot/app/requirements.txt

# Копируем весь src внутрь контейнера
COPY src/bot .

# Команда запуска бота
CMD ["python", "-m", "bot.app.main"]