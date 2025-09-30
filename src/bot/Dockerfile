# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /bot

# Копируем requirements в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота внутрь контейнера
COPY app ./app

# Команда запуска бота
CMD ["python", "app/main.py"]
