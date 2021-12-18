COMPOSE ?= docker-compose -f docker-compose.yml

run: build
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs

rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

