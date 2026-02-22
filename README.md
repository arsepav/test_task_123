# REST API приложения для справочника Организаций, Зданий, Деятельности


Чтобы запустить приложение
```bash
docker compose up --build
```
это создаст базу данных (postgres), и проведет миграции

API доступно по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

Все запросы к API (кроме `/health`) требуют заголовок **X-API-Key**. Значение по умолчанию: `tmp-api-key`

## Методы API


- **GET** `/organizations/building/{building_id}` — список организаций в указанном здании
- **GET** `/organizations/activity/{activity_id}` — организации по виду деятельности
- **GET** `/organizations/nearby` — организации в радиусе или в прямоугольной области (параметры: `lat`, `lon`, `radius_km` или `lat_min`, `lat_max`, `lon_min`, `lon_max`)
- **GET** `/organizations/{organization_id}` — информация об организации по ID
- **GET** `/organizations/search/activity?activity_id=` — поиск организаций по виду деятельности с учётом поддерева (например, «Еда» → Еда, Мясная продукция, Молочная продукция)
- **GET** `/organizations/search/name?q=` — поиск организаций по названию
- **GET** `/buildings` — список зданий (опционально с фильтром по области/радиусу)


## Пример запроса с API-ключом

```bash
curl -H "X-API-Key: tmp-api" http://localhost:8000/organizations/1
```

можно проверить все ручки запустив клиент:
```bash
python client.py
```


---
Код в `app/`: models (таблицы), routers (organizations, buildings), schemas, services. database/config/dependencies/main — сессия, настройки, api-key, точка входа.

alembic — миграции. versions: 001 схема, 002 сиды из json. Конфиг alembic.ini, env.py тянет метаданные из app. При compose up миграции запускаются
