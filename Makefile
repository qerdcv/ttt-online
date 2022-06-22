COMPOSE ?= docker-compose -f ops/docker-compose.base.yml
COMPOSE_DEV ?= $(COMPOSE) -f ops/docker-compose.dev.yml -p ttto-dev
COMPOSE_TEST ?= $(COMPOSE) -f ops/docker-compose.test.yml -p ttto-test

APP_DB_USERNAME ?= postgres
APP_DB_PASSWORD ?= postgres
APP_DB_DATABASE ?= postgres
APP_SECRET ?= A55iwGUdDMUlBM1VpbkivhAssGW2f1Qclknipse11Gg=

.EXPORT_ALL_VARIABLES:

.PHONY: help
.DEFAULT_GOAL: help

help: ## Show help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Build and start containers
	$(COMPOSE_DEV) up --build --force-recreate -d
	@echo http://localhost:4444

logs: ## Attach to the containers logs
	$(COMPOSE_DEV) logs -f

rm: ## Remove containers
	$(COMPOSE_DEV) rm -sfv

lint: ## Run lint for python
	flake8

setup-testenv: ## Setup test environment (currently only database)
	docker run --name test-db \
	-e POSTGRES_USER=test \
	-e POSTGRES_PASSWORD=test \
	-e POSTGRES_DB=test \
	-p 5433:5432 \
	-d \
	postgres:latest

cleanup-testenv: ## Clenup test environment
	docker rm -f test-db

test-integration: ## Build test image and run test containers
	$(COMPOSE_TEST) up --build --abort-on-container-exit
	$(COMPOSE_TEST) rm -fsv
