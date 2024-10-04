# Используйте базовый образ Python
FROM python:3.10-slim

# Установите необходимые пакеты
RUN apt-get update && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установите часовой пояс
RUN ln -s -f /usr/share/zoneinfo/Etc/GMT /etc/localtime

# Установка переменной окружения
ENV PYTHONUNBUFFERED=1

# Определение рабочей директории
WORKDIR /app

# Скопируйте все файлы из папки Moderator в рабочую директорию контейнера
COPY . /app

# Скопируйте requirements.txt и установите зависимости
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Определение базовой команды
CMD ["python", "app.py"]
