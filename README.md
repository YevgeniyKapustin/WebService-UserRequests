## Запуск продакшена
Прежде всего следует разобраться с конфигом. Можете переменовать его: `mv default.env .env`, либо прописать в докере ссылку на `default.env` в конфиге, вместо `.env` или создать и скопировать содержимое в файл `.env`.

1. Через docker 
    ```bash
    docker-compose up  
    ```

2. Напрямую через uvicorn
    Потребуется вручную запускать `run_migrations.sh`, установливать зависимости из poetry, устанавливать все необходимые сервисы локально, я думаю этот продолжительный процесс не обязательно разжёвывать, поскольку предполагается использование docker.
    ```bash
    python run.py
    ```
## Запуск тестов
Запуск тестов осущевляется исключительно через docker
```bash
docker-compose -f docker-compose.tests.yml up
```
Не обязательно это потребуется, но логи тестов можно посмотреть этой командой:  `# todo: сделать волюм с логами` 
```bash
docker logs --tail 1000 webservice-userrequests_test_app_1
```


## Примеры запросов и ответов

Все запросы сделаны через swagger, который по умолчанию запускается на http://0.0.0.0:8000/docs

1. 
    - Запрос
        ```bash
        curl -X 'GET' \
        'http://0.0.0.0:8000/api/v1/applications?username=Pro100Vasya&page=2&size=3' \
        -H 'accept: application/json'
        ```
    - Ответ
        ```json
            [
                {
                    "id": 41,
                    "username": "Pro100Vasya",
                    "description": "Kvadrobery invade in my home",
                    "created_at": "2025-01-21T08:16"
                },
                {
                    "id": 42,
                    "username": "Pro100Vasya",
                    "description": "Kvadrobery invade in my home",
                    "created_at": "2025-01-21T08:16"
                },
                {
                    "id": 43,
                    "username": "Pro100Vasya",
                    "description": "Kvadrobery invade in my home",
                    "created_at": "2025-01-21T08:16"
                }
            ]
        ```
2. 
    - Запрос
        ```bash
        curl -X 'POST' \
        'http://0.0.0.0:8000/api/v1/applications' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "username": "Pro100Vasya",
        "description": "Kvadrobery invade in my home"
        }'```
    - Ответ
        ```json
        {
            "message": "Create",
            "description": "Создано"
        }
        ```

## Задание

Разработайте сервис для обработки заявок пользователей. Сервис должен:
1. Принимать заявки через REST API (FastAPI).
2. Обрабатывать и записывать заявки в PostgreSQL.
3. Публиковать информацию о новых заявках в Kafka.
4. Обеспечивать эндпоинт для получения списка заявок с фильтрацией и пагинацией.
5. Включать Docker-файл для развертывания приложения.

---

### Детали реализации

1. REST API
    - Создайте эндпоинт POST /applications для создания новой заявки. Заявка содержит следующие поля:
        - id (генерируется автоматически)
        - user_name (имя пользователя)
        - description (описание заявки)
        - created_at (дата и время создания, устанавливается автоматически)

    - Создайте эндпоинт GET /applications для получения списка заявок:
        - Поддержка фильтрации по имени пользователя (user_name).
        - Поддержка пагинации (параметры page и size).

2. PostgreSQL:
    - Спроектируйте таблицу для хранения заявок.
    - Используйте SQLAlchemy для работы с базой данных.

3. Kafka:
    - Настройте публикацию данных о новых заявках в топик Kafka.
    - В сообщении должно содержаться:
        - id заявки
        - user_name
        - description
        - created_at

4. Асинхронность:
    - Убедитесь, что все взаимодействия с Kafka и PostgreSQL реализованы асинхронно.

5. Docker:
- Подготовьте Dockerfile и docker-compose.yml для локального запуска:
    - Приложение (FastAPI)
    - PostgreSQL
    - Kafka

6. Документация:
- Опишите инструкцию по запуску проекта.
- Добавьте пример запроса и ответа для эндпоинтов.

---

Дополнительно
Реализованные дополнительные функции будут преимуществом:
- Валидация входящих данных с использованием Pydantic.
- Логирование ошибок и событий в приложении.
- Подготовка unit-тестов для ключевых компонентов.

### Срок выполнения:
Предоставьте решение в течение 7 дней.
