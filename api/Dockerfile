FROM python:3.10-slim

# 1. Рабочая директория внутри контейнера
WORKDIR /app

# 2. Системные зависимости (нужны для asyncpg)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Копируем requirements
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь код API
COPY . .

# 6. Открываем порт
EXPOSE 8000

# 7. Запуск FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
