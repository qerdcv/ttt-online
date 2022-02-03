COMPOSE ?= docker-compose -f docker-compose.yml

run: build
	$(COMPOSE) up -d
	echo http://localhost:4444

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs

rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

