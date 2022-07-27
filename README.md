
# Бот для чата @natural_language_processing. Удаляет технические сообщения "тебе в группе", "покинул группу"

## Разработка, лог команд

Создать директорию в YC.

```bash
yc resource-manager folder create --name natasha-vagif-bot
```

Создать сервисный аккаунт в YC. Записать `id` в `.env`.

```bash
yc iam service-accounts create natasha-vagif-bot --folder-name natasha-vagif-bot

id: {SERVICE_ACCOUNT_ID}
```

Создать реестр для контейнера в YC. Записать `id` в `.env`.

```bash
yc container registry create default --folder-name natasha-vagif-bot

id: {REGISTRY_ID}
```

Дать права сервисному аккаунту читать из реестра. Интеграция с YC Serverless Container.

```bash
yc container registry add-access-binding default \
  --role container-registry.images.puller \
  --service-account-name natasha-vagif-bot \
  --folder-name natasha-vagif-bot
```

Создать Serverless Container. Записать `id` в `.env`.

```bash
yc serverless container create --name default --folder-name natasha-vagif-bot

id: {CONTAINER_ID}
```

Разрешить без токена. Телеграм дергает вебхук.

```bash
yc serverless container allow-unauthenticated-invoke default \
  --folder-name natasha-vagif-bot
```

Логи.

```bash
yc log read default --follow --folder-name natasha-vagif-bot
```

Прицепить вебхук.

```bash
WEBHOOK_URL=https://${CONTAINER_ID}.containers.yandexcloud.net/
curl --url https://api.telegram.org/bot${BOT_TOKEN}/setWebhook\?url=${WEBHOOK_URL}
```

Трюк чтобы загрузить окружение из `.env`.

```bash
export $(cat .env | xargs)
```

Установить зависимости для тестов.

```bash
pip install \
  pytest-aiohttp \
  pytest-asyncio \
  pytest-flakes \
  pytest-pycodestyle
```

Прогнать линтер, тесты.

```bash
make test-lint test-key KEY=test
```

Собрать образ, загрузить его в реестр, задер

```bash
make image push deploy
```
