FROM python:3.12-slim

# Установка переменных окружения
ENV BOT_NAME=tgbot
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Установка poetry
RUN pip install -U pip && pip install poetry

# Установка основных элементов сборки
RUN apt-get update && apt-get install -y build-essential

# Установка рабочей директории
WORKDIR /usr/src/app/${BOT_NAME}

# Копируются только файлы конфигурации poetry
COPY pyproject.toml poetry.lock /usr/src/app/${BOT_NAME}/

# Установка зависимостей проекта с помощью poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копирование всего проекта
COPY . /usr/src/app/${BOT_NAME}