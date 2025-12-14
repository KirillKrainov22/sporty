FROM python:3.10-slim

# 1. Рабочая директория
WORKDIR /app

# 2. Копируем зависимости
COPY requirements.txt .
# 3. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем код бота
COPY . .

# 5. Запуск бота

CMD ["python", "src/main.py"]

