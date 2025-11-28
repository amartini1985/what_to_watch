# 1. Используем официальный образ Python как основу
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /opinions_app

# 3. Копируем файл с зависимостями и устанавливаем их (используем кэш)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь остальной код приложения
COPY . .

# 5. "Сообщаем" Docker, что наше приложение будет работать на порту 5000
EXPOSE 5000

# 6. Указываем команду, которая запустится при старте контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "opinions_app.wsgi:app"]

# docker run --rm -d -p 5000:5000 --name backend backend