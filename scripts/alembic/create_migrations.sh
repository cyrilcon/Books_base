#!/bin/bash

echo "Enter name of migration: "
read message
source .env
docker exec ${BOT_CONTAINER_NAME} alembic revision --autogenerate -m "$message"