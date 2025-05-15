# Инструкция по запуску:
1. Создать `.env` файл по примеру из файла `.env.example`
2. Собрать и запустить контейнер, используя команды:
    1. `docker build -t tech_avoidedabsence .`
    2. `export $(grep -v '^#' .env | xargs)`
    2. `docker run -v $(pwd)/$DB_PATH:/src/$DB_PATH --env-file .env tech_avoidedabsence` *(Linux)*