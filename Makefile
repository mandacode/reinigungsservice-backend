SERVICE=fastapi

.PHONY: up lint format test migrate encode-creds


up:
	docker compose up --build

lint:
	docker compose exec $(SERVICE) ruff check --fix app

format:
	docker compose exec $(SERVICE) ruff format app

test:
	docker compose exec $(SERVICE) pytest

revision:
	docker compose exec $(SERVICE) alembic revision --autogenerate

migrate:
	docker compose exec $(SERVICE) alembic upgrade head

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f $(SERVICE)

bash:
	docker compose exec $(SERVICE) bash

encode-googleapi-creds:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE variable is not set. Usage: make encode-creds FILE=path/to/file.json"; \
		exit 1; \
	fi
	base64 -i $(FILE) > google_credentials_base64.txt | tr -d '\n'
	echo "Encoded $(FILE) to google_credentials_base64.txt"
