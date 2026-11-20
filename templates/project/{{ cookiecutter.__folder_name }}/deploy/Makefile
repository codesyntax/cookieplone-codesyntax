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

# The image tag comes from the repository CalVer file. Exporting it makes every
# `docker compose` command in this deploy directory use the released tag.
VERSION ?= $(shell head -n 1 ../version.txt 2>/dev/null)
export VERSION

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## Show the purpose of all commands
	@echo "All available commands:"
	@echo "-----------------------"
	@grep -Eh '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'

.PHONY: help-summary
help-summary: ## Show the purpose of relevant commands (start, stop, restart, logs, ...)
	@echo "Useful commands:"
	@echo "----------------"
	@grep -Eh '^[a-zA-Z_-]*(logs|restart|start|status|stop)[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'

.PHONY: version
version: ## Show the image version used by docker compose
	@echo "$(VERSION)"

.PHONY: previous-version
previous-version: ## Show the previous released version, taken from the git tags
	@git tag --sort=-v:refname 2>/dev/null | awk 'BEGIN { v = "$(VERSION)" } !found && (v == "" || $$0 != v) { print; found = 1 }'

.PHONY: latest-versions
latest-versions: ## Show the latest 5 released versions, taken from the git tags
	@git tag --sort=-v:refname 2>/dev/null | awk 'NR <= 5'

.PHONY: pull
pull: ## git pull the current branch (fast-forward only)
	@echo "$(GREEN) ===> Pulling"
	git pull --ff-only

# ---------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------
.PHONY: start
start: ## Start all services
	docker compose up -d

.PHONY: start-fg
start-fg: ## Start all services in foreground
	docker compose up

.PHONY: start-caddy
start-caddy: ## Start caddy
	docker compose up caddy -d

.PHONY: start-nginx
start-nginx: ## Start nginx
	docker compose up nginx -d

.PHONY: start-backend
start-backend: ## Start backend
	docker compose up backend -d

{%- if cookiecutter.feature_headless %}

.PHONY: start-frontend
start-frontend: ## Start frontend
	docker compose up frontend -d
{%- endif %}

{%- if cookiecutter.devops_cache %}
{%- if cookiecutter.feature_headless %}

.PHONY: start-varnish-frontend
start-varnish-frontend: ## Start varnish-frontend
	docker compose up varnish-frontend -d
{%- endif %}

.PHONY: start-varnish-backend
start-varnish-backend: ## Start varnish-backend
	docker compose up varnish-backend -d
{%- endif %}

{%- if cookiecutter.postgres %}

.PHONY: start-postgres
start-postgres: ## Start postgres
	docker compose up postgres -d

{%- if cookiecutter.thumbor %}

.PHONY: start-thumbor
start-thumbor: ## Start thumbor
	docker compose up thumbor -d
{%- endif %}
{%- else %}

.PHONY: start-zeo
start-zeo: ## Start zeo
	docker compose up zeo -d
{%- endif %}

.PHONY: start-anubis
start-anubis: ## Start anubis
	docker compose up anubis -d

.PHONY: start-cron-runner
start-cron-runner: ## Start cron-runner
	docker compose up cron-runner -d

# ---------------------------------------------------------------------------
# Stop
# ---------------------------------------------------------------------------
.PHONY: stop
stop: ## Stop all services
	@echo "$(RED) ===> Stopping"
	docker compose stop

.PHONY: stop-caddy
stop-caddy: ## Stop caddy
	docker compose stop caddy

.PHONY: stop-nginx
stop-nginx: ## Stop nginx
	docker compose stop nginx

.PHONY: stop-backend
stop-backend: ## Stop backend
	docker compose stop backend

{%- if cookiecutter.feature_headless %}

.PHONY: stop-frontend
stop-frontend: ## Stop frontend
	docker compose stop frontend
{%- endif %}

{%- if cookiecutter.devops_cache %}
{%- if cookiecutter.feature_headless %}

.PHONY: stop-varnish-frontend
stop-varnish-frontend: ## Stop varnish-frontend
	docker compose stop varnish-frontend
{%- endif %}

.PHONY: stop-varnish-backend
stop-varnish-backend: ## Stop varnish-backend
	docker compose stop varnish-backend
{%- endif %}

{%- if cookiecutter.postgres %}

.PHONY: stop-postgres
stop-postgres: ## Stop postgres
	docker compose stop postgres

{%- if cookiecutter.thumbor %}

.PHONY: stop-thumbor
stop-thumbor: ## Stop thumbor
	docker compose stop thumbor
{%- endif %}
{%- else %}

.PHONY: stop-zeo
stop-zeo: ## Stop zeo
	docker compose stop zeo
{%- endif %}

.PHONY: stop-anubis
stop-anubis: ## Stop anubis
	docker compose stop anubis

.PHONY: stop-cron-runner
stop-cron-runner: ## Stop cron-runner
	docker compose stop cron-runner

# ---------------------------------------------------------------------------
# Restart
# ---------------------------------------------------------------------------
.PHONY: restart
restart: ## Restart all services
	docker compose restart

.PHONY: restart-caddy
restart-caddy: ## Restart caddy
	docker compose restart caddy

.PHONY: restart-nginx
restart-nginx: ## Restart nginx
	docker compose restart nginx

.PHONY: restart-backend
restart-backend: ## Restart backend
	docker compose restart backend

{%- if cookiecutter.feature_headless %}

.PHONY: restart-frontend
restart-frontend: ## Restart frontend
	docker compose restart frontend
{%- endif %}

{%- if cookiecutter.devops_cache %}
{%- if cookiecutter.feature_headless %}

.PHONY: restart-varnish-frontend
restart-varnish-frontend: ## Restart varnish-frontend
	docker compose restart varnish-frontend
{%- endif %}

.PHONY: restart-varnish-backend
restart-varnish-backend: ## Restart varnish-backend
	docker compose restart varnish-backend

.PHONY: restart-varnish
restart-varnish: ## Restart all varnish services
	docker compose restart varnish-backend
	{%- if cookiecutter.feature_headless %}
	docker compose restart varnish-frontend
	{%- endif %}
{%- endif %}

{%- if cookiecutter.postgres %}

.PHONY: restart-postgres
restart-postgres: ## Restart postgres
	docker compose restart postgres

{%- if cookiecutter.thumbor %}

.PHONY: restart-thumbor
restart-thumbor: ## Restart thumbor
	docker compose restart thumbor
{%- endif %}
{%- else %}

.PHONY: restart-zeo
restart-zeo: ## Restart zeo
	docker compose restart zeo
{%- endif %}

.PHONY: restart-anubis
restart-anubis: ## Restart anubis
	docker compose restart anubis

.PHONY: restart-cron-runner
restart-cron-runner: ## Restart cron-runner
	docker compose restart cron-runner

# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------
.PHONY: logs
logs: ## Show logs of all services
	docker compose logs -f --tail=200

.PHONY: logs-caddy
logs-caddy: ## Show caddy logs
	docker compose logs -f --tail=200 caddy

.PHONY: logs-nginx
logs-nginx: ## Show nginx logs
	docker compose logs -f --tail=200 nginx

.PHONY: logs-backend
logs-backend: ## Show backend logs
	docker compose logs -f --tail=200 backend

{%- if cookiecutter.feature_headless %}

.PHONY: logs-frontend
logs-frontend: ## Show frontend logs
	docker compose logs -f --tail=200 frontend
{%- endif %}

{%- if cookiecutter.devops_cache %}
{%- if cookiecutter.feature_headless %}

.PHONY: logs-varnish-frontend
logs-varnish-frontend: ## Show varnish-frontend logs
	docker compose logs -f --tail=200 varnish-frontend
{%- endif %}

.PHONY: logs-varnish-backend
logs-varnish-backend: ## Show varnish-backend logs
	docker compose logs -f --tail=200 varnish-backend
{%- endif %}

{%- if cookiecutter.postgres %}

.PHONY: logs-postgres
logs-postgres: ## Show postgres logs
	docker compose logs -f --tail=200 postgres

{%- if cookiecutter.thumbor %}

.PHONY: logs-thumbor
logs-thumbor: ## Show thumbor logs
	docker compose logs -f --tail=200 thumbor
{%- endif %}
{%- else %}

.PHONY: logs-zeo
logs-zeo: ## Show zeo logs
	docker compose logs -f --tail=200 zeo
{%- endif %}

.PHONY: logs-anubis
logs-anubis: ## Show anubis logs
	docker compose logs -f --tail=200 anubis

.PHONY: logs-cron-runner
logs-cron-runner: ## Show cron-runner logs
	docker compose logs -f --tail=200 cron-runner

# .PHONY: build-scripts
# build-scripts: ## Show cron-runner logs
# 	docker compose build --no-cache scripts

.PHONY: upgrade
upgrade: pull crons ## Download the new images and recreate backend and frontend services
{%- if cookiecutter.feature_headless %}
	docker compose pull backend frontend
	docker compose up -d backend frontend
{%- else %}
	docker compose pull backend
	docker compose up -d backend
{%- endif %}

.PHONY: full-upgrade
full-upgrade: pull crons ## Download the new images and recreate all services
	docker compose pull
	docker compose up -d --remove-orphans

.PHONY: deploy
deploy: upgrade

.PHONY: full-deploy
full-deploy: full-upgrade

.PHONY: crons
crons: restart-cron-runner ## set all the cron jobs defined in crons.txt in the local crontab
	( (crontab -l 2>/dev/null || true; cat crons.txt) | sort -u) | crontab -

{% raw %}
.PHONY: status
status: ## Check the status and health of the services
	@ { set +x; } 2>/dev/null; \
	echo "Status of the services:"; \
	echo "-----------------------"; \
	for service in $$(docker compose config --services | sort); do \
		container_id=$$(docker compose ps -q "$${service}" 2>/dev/null || true); \
		if [ -z "$${container_id}" ]; then \
			echo "ERROR: $${service} (not running)"; \
			continue; \
		fi; \
		state=$$(docker inspect -f '{{.State.Status}}' "$${container_id}"); \
		health=$$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' "$${container_id}"); \
		if [ "$${state}" = "running" ] && { [ -z "$${health}" ] || [ "$${health}" = "healthy" ]; }; then \
			echo "OK: $${service} ($${state}$${health:+, $$health})"; \
		elif [ "$${state}" = "running" ]; then \
			echo "WARN: $${service} ($${state}, health: $${health})"; \
		else \
			echo "ERROR: $${service} ($${state})"; \
		fi \
	done
{% endraw %}

# No modifications are allowed in this Makefile
# use the scripts/Makefile to add custom commands

include scripts/Makefile
