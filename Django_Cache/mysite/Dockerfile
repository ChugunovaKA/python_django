# Используем официальный Python 3.10 slim
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы управления зависимостями
COPY Pipfile Pipfile.lock /app/

# Устанавливаем pipenv
RUN pip install --no-cache-dir pipenv

# Устанавливаем зависимости в системное окружение (без виртуального)
RUN pipenv install --deploy --system

# Копируем весь проект в контейнер
COPY . /app/

# Переменная окружения для работы статики
ENV DJANGO_DEBUG=1

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение через Gunicorn (замени mysite на имя своей папки, если другое)
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
