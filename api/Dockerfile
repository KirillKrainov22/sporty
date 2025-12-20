FROM python:3.10-slim

# 1. Рабочая директория внутри контейнера
WORKDIR /app

# 2. Копируем ТОЛЬКО requirements.txt из папки api
COPY requirements.txt .

# 3. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем ВЕСЬ код API
COPY . .

# 5. Открываем порт FastAPI
EXPOSE 8000

# 6. Запуск FastAPI
CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]