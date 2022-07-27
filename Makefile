IMAGE = natasha-vagif-bot
REGISTRY = cr.yandex/$(REGISTRY_ID)
REMOTE = $(REGISTRY)/$(IMAGE)

test-lint:
	pytest -vv --asyncio-mode=auto --pycodestyle --flakes main.py

test-key:
	pytest -vv --asyncio-mode=auto -s -k $(KEY) test.py

image:
	docker build -t $(IMAGE) .

push:
	docker tag $(IMAGE) $(REMOTE)
	docker push $(REMOTE)

deploy:
	yc serverless container revision deploy \
		--container-name default \
		--image $(REGISTRY)/natasha-vagif-bot:latest \
		--cores 1 \
		--memory 256MB \
		--concurrency 16 \
		--execution-timeout 30s \
		--environment BOT_TOKEN=$(BOT_TOKEN) \
		--service-account-id $(SERVICE_ACCOUNT_ID) \
		--folder-name natasha-vagif-bot
