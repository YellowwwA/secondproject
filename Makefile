.PHONY: build up down logs fastapi nodejs

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