.PHONY: build up down logs fastapi nodejs push deploy

IMAGE_NAME=kibwa14/secondproject
TAG=latest

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps -a

img:
	docker compose images

rm:
	docker compose rm -f -v

rmi:
	docker image prune -a -f

push:
	docker tag your-container-name $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):$(TAG)

deploy: build push