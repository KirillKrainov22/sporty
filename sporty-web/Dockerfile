FROM python:3.10-slim

# устанавливаем рабочую директорию
WORKDIR /app

# копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код
COPY . .

# Streamlit слушает порт 8501
EXPOSE 8501

# запуск Streamlit; предполагаем, что основной файл называется main.py
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
