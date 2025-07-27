SERVICE=fastapi

.PHONY: up lint format test migrate

up:
	docker compose up --build

lint:
	docker compose exec $(SERVICE) ruff check .

format:
	docker compose exec $(SERVICE) ruff format .

test:
	docker compose exec $(SERVICE) pytest

migrate:
	docker compose exec $(SERVICE) alembic upgrade head

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f $(SERVICE)

bash:
	docker compose exec $(SERVICE) bash