#!/bin/bash

source .env
docker exec ${BOT_CONTAINER_NAME} alembic upgrade head