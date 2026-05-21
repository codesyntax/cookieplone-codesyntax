### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## Show the purpose of all commands
	@echo "All available commands:"
	@echo "-----------------------"
	@grep -Eh '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: help-summary
help-summary: ## Show the purpose of relevant commands (start, restart, stop, ...)
	@echo "Useful commands:"
	@echo "----------------"
	@grep -Eh '^[a-zA-Z_-]*(restart|start|status|stop)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: pull
pull: ## git pull repo main branch
	@echo "$(GREEN) ===> Pulling"
	git pull origin main

.PHONY: stop
stop: ## Stop all services
	@echo "$(RED) ===> Stopping"
	docker compose down

.PHONY: start
start: ## Start all services
	docker compose up -d

.PHONY: start-fg
start-fg: ## Start in foreground
	docker compose up

.PHONY: restart
restart: ## Restart all services
	docker compose down
	docker compose up -d

.PHONY: restart-nginx
restart-nginx: ## Restart nginx
	docker compose down nginx
	docker compose up nginx -d

{%- if cookiecutter.feature_headless %}
.PHONY: restart-frontend
restart-frontend: ## Restart frontend
	docker compose down frontend
	docker compose up frontend -d
{%- endif %}

.PHONY: restart-backend
restart-backend: ## Restart backend
	docker compose down backend
	docker compose up backend -d

{%- if cookiecutter.devops_cache %}
.PHONY: restart-varnish
restart-varnish: ## Restart varnish
	docker compose down varnish-backend
	{%- if cookiecutter.feature_headless %}
	docker compose down varnish-frontend
	docker compose up varnish-frontend -d
	{%- endif %}
	docker compose up varnish-backend -d
{%- endif %}

.PHONY: restart-cron-runner
restart-cron-runner: ## Restart cron-runner
	docker compose down cron-runner
	docker compose up cron-runner -d

.PHONY: logs-nginx
logs-nginx: ## Show nginx logs
	docker compose logs -f nginx

.PHONY: logs-backend
logs-backend: ## Show backend logs
	docker compose logs -f backend

{%- if cookiecutter.feature_headless %}
.PHONY: logs-frontend
logs-frontend: ## Show frontend logs
	docker compose logs -f frontend
{%- endif %}

{%- if cookiecutter.postgres %}
.PHONY: restart-postgres
restart-postgres: ## Restart postgres
	docker compose down postgres
	docker compose up postgres -d

.PHONY: logs-postgres
logs-postgres: ## Show postgres logs
	docker compose logs -f postgres

{%- if cookiecutter.thumbor %}
.PHONY: restart-thumbor
restart-thumbor: ## Restart thumbor
	docker compose down thumbor
	docker compose up thumbor -d

.PHONY: logs-thumbor
logs-thumbor: ## Show thumbor logs
	docker compose logs -f thumbor
{%- endif %}

{%- endif %}
.PHONY: logs-cron-runner
logs-cron-runner: ## Show cron-runner logs
	docker compose logs -f cron-runner

# .PHONY: build-scripts
# build-scripts: ## Show cron-runner logs
# 	docker compose build --no-cache scripts

.PHONY: upgrade
# upgrade: pull crons build-scripts ## Download the new images, build scripts and restart backend and frontend services
upgrade: pull crons ## Download the new images and restart backend and frontend services
	docker compose pull
	docker compose down backend
    {%- if cookiecutter.feature_headless %}
	docker compose down frontend
	docker compose up frontend -d
    {%- endif %}
	docker compose up backend -d

.PHONY: full-upgrade
# full-upgrade: pull crons build-scripts ## Download the new images, build scripts and restart all services
full-upgrade: pull crons ## Download the new images and restart all services
	docker compose pull
	docker compose down
	docker compose up -d

.PHONY: deploy
deploy: upgrade

.PHONY: full-deploy
full-deploy: full-upgrade

.PHONY: crons
crons: restart-cron-runner ## set all the cron jobs defined in crons.txt in the local crontab
	( (crontab -l 2>/dev/null || true; cat crons.txt) | sort -u) | crontab -

.PHONY: check the status of the services
status:
	@ { set +x; } 2>/dev/null; \
	echo "Status of the services:"; \
	echo "-----------------------"; \
	for service in $$(docker compose config --services | sort); do \
		if [ -z "$$(docker compose ps -q $${service})" ]; then \
		echo "❌ ERROR: '$${service}'"; \
		else \
		echo "✅ OK: $${service}"; \
		fi \
	done

# No modifications are allowed in this Makefile
# use the scripts/Makefile to add custom commands

include scripts/Makefile
