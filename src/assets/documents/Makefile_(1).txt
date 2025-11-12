# SPLANTS Marketing Engine - Makefile
# Convenient commands for development and deployment

.PHONY: help
help: ## Show this help message
	@echo "SPLANTS Marketing Engine - Command Reference"
	@echo "============================================"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Initial setup - copy env file and build
	@echo "Setting up SPLANTS Marketing Engine..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file - please add your API keys"; fi
	@docker-compose build
	@echo "Setup complete! Run 'make start' to begin"

.PHONY: start
start: ## Start all services
	@echo "Starting SPLANTS Marketing Engine..."
	@docker-compose up -d
	@echo "Services starting... Access at http://localhost:8080"
	@echo "API Docs: http://localhost:8080/docs"

.PHONY: stop
stop: ## Stop all services
	@echo "Stopping services..."
	@docker-compose down

.PHONY: restart
restart: ## Restart all services
	@echo "Restarting services..."
	@docker-compose restart

.PHONY: logs
logs: ## View application logs
	@docker-compose logs -f app

.PHONY: logs-all
logs-all: ## View all service logs
	@docker-compose logs -f

.PHONY: status
status: ## Check service status
	@docker-compose ps

.PHONY: clean
clean: ## Remove containers and volumes (WARNING: deletes data)
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] && docker-compose down -v

.PHONY: backup
backup: ## Backup database
	@echo "Creating database backup..."
	@mkdir -p backups
	@docker-compose exec db pg_dump -U splants splants > backups/backup-$$(date +%Y%m%d-%H%M%S).sql
	@echo "Backup saved to backups/"

.PHONY: shell
shell: ## Open Python shell in app container
	@docker-compose exec app python

.PHONY: db-shell
db-shell: ## Open PostgreSQL shell
	@docker-compose exec db psql -U splants splants

.PHONY: test-api
test-api: ## Test API with sample request
	@echo "Testing content generation..."
	@curl -X POST "http://localhost:8080/v1/generate" \
		-H "X-API-Key: change-this-to-a-secure-password-123" \
		-H "Content-Type: application/json" \
		-d '{"content_type": "blog", "topic": "Test: 5 AI Tips", "tone": "professional", "length": 200}'

.PHONY: update
update: ## Pull latest changes and rebuild
	@echo "Updating SPLANTS Marketing Engine..."
	@docker-compose pull
	@docker-compose build --no-cache
	@docker-compose up -d
	@echo "Update complete!"

.PHONY: dev
dev: ## Start in development mode with hot-reload
	@docker-compose up

.PHONY: redis-enable
redis-enable: ## Enable Redis caching
	@echo "Enabling Redis cache..."
	@sed -i.bak 's/# redis:/redis:/g' docker-compose.yml
	@sed -i.bak 's/# redis_data:/redis_data:/g' docker-compose.yml
	@echo "Redis enabled. Add REDIS_URL=redis://redis:6379 to .env"
	@echo "Run 'make restart' to apply changes"

.PHONY: monitor
monitor: ## Monitor resource usage
	@docker stats