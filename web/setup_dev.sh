#!/bin/bash
echo "=== Sporty Web Dev Setup ==="

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Создание виртуального окружения
echo "Creating virtual environment..."
python3 -m venv venv

# Активация (инструкция)
echo ""
echo "To activate virtual environment:"
echo "  On Mac/Linux: source venv/bin/activate"
echo "  On Windows:   venv\\Scripts\\activate.bat"
echo ""
echo "Then install dependencies: pip install -r requirements.txt"
echo "And run: streamlit run app.py"
