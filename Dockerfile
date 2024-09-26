FROM python:3.12-slim

# Set environment variables
ENV BOT_NAME=tgbot
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Setting poetry
RUN pip install -U pip && pip install poetry

# Installing the basic elements of the assembly
RUN apt-get update && apt-get install -y build-essential

# Setting the working directory
WORKDIR /usr/src/app/${BOT_NAME}

# Only the poetry configuration files are copied
COPY pyproject.toml poetry.lock /usr/src/app/${BOT_NAME}/

# Install project dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copying the entire project
COPY . /usr/src/app/${BOT_NAME}