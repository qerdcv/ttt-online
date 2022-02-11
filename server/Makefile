COMPOSE ?= docker-compose -f docker-compose.yml
APP_DB_USERNAME ?= postgres
APP_DB_PASSWORD ?= postgres
APP_DB_DATABASE ?= postgres

.EXPORT_ALL_VARIABLES:

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

