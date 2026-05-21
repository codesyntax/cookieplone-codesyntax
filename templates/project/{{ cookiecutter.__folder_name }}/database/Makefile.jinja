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

.PHONY: stop
stop: ## Stop all services
	@echo "$(RED) ===> Stopping"
	docker compose down

.PHONY: start
start: ## Start all services
	docker compose up

.PHONY: zodb-convert
zodb-convert: ## Convert a Filestorage to zodb-pgjsonb
	uvx --with="zodb_pgjsonb" zodb-convert convert.conf -v

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

