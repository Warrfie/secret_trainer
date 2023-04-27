#!/bin/bash

# Загрузить изменения из удаленного Git-репозитория
git pull

# Остановить контейнеры web, app и mongo_db, если они существуют
docker stop web app mongo_db || true

# Удалить контейнеры web, app и mongo_db, если они существуют
docker rm web app mongo_db || true

# Удалить сеть custom, если она существует
docker network rm custom || true

# Удалить образы app и mongo:4.4, если они существуют
docker rmi app mongo:4.4 || true

# Запустить контейнеры, используя docker и файл docker.yaml
docker compose -f docker.yaml up -d

# Включить автозапуск для контейнеров web, app и mongo_db с флагом "unless-stopped"
docker update --restart=unless-stopped web app mongo_db