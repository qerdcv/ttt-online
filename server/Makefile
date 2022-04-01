COMPOSE ?= docker-compose -f docker-compose.yml
COMPOSE_TEST ?= $(COMPOSE) -f docker-compose.test.yml

APP_DB_USERNAME ?= postgres
APP_DB_PASSWORD ?= postgres
APP_DB_DATABASE ?= postgres
APP_SECRET ?= A55iwGUdDMUlBM1VpbkivhAssGW2f1Qclknipse11Gg=

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

test-integration: build_test
	$(COMPOSE_TEST) up --abort-on-container-exit
	$(COMPOSE_TEST) rm -f

build_test:
	$(COMPOSE_TEST) build
