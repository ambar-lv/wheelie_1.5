# !/bin/bash

# Скрипт для очистки Django-проекта:
# 1. Удаляет все файлы миграций (кроме __init__.py)
# 2. Удаляет все папки __pycache__
# 3. Удаляет базу данных SQLite

echo "Начинаем очистку Django-проекта..."

# Удаление файлов миграций
echo "Удаление файлов миграций..."
find . -path "*/apps/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/apps/*/migrations/*.pyc" -delete
echo "Файлы миграций удалены."

# Удаление папок __pycache__
echo "Удаление папок __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "Папки __pycache__ удалены."

echo "Очистка завершена успешно!"