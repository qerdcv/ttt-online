COMPOSE ?= docker-compose -f docker-compose.base.yml
COMPOSE_DEV ?= $(COMPOSE) -f docker-compose.dev.yml -p ttto-dev
COMPOSE_TEST ?= $(COMPOSE) -f docker-compose.test.yml -p ttto-test

APP_DB_USERNAME ?= postgres
APP_DB_PASSWORD ?= postgres
APP_DB_DATABASE ?= postgres
APP_SECRET ?= A55iwGUdDMUlBM1VpbkivhAssGW2f1Qclknipse11Gg=

.EXPORT_ALL_VARIABLES:

run: build
	$(COMPOSE_DEV) up -d
	echo http://localhost:4444

build:
	$(COMPOSE_DEV) build

logs:
	$(COMPOSE_DEV) logs -f

rm:
	$(COMPOSE_DEV) rm -sfv

test-integration: build_test
	$(COMPOSE_TEST) up  --abort-on-container-exit
	$(COMPOSE_TEST) rm -fv

build_test:
	$(COMPOSE_TEST) build
