# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app/src

# Копируем корневой requirements проекта (если есть общий)
COPY requirements.txt /backend/app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /backend/app/requirements.txt

# Копируем весь src внутрь контейнера
COPY src/backend .

# Экспонируем порт приложения
EXPOSE 8000

# Команда запуска FastAPI через uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
