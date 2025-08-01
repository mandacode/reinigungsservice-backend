# 🧽 Reinigungsservice API

**Reinigungsservice API** is a FastAPI-based backend for managing a cleaning services platform.  
It includes customer management, employee and work tracking, authentication, and document generation.

---

## 📁 Project Structure
```plaintext
reinigungsservice-backend/
├── app/ # Main application package
│ ├── api/ # FastAPI route definitions
│ ├── config.py # App-level configuration
│ ├── database/ # DB connection, ORM models, and migrations
│ ├── dependencies.py # Reusable dependencies for DI
│ ├── main.py # Entry point
│ ├── models/ # Pydantic models and data validation
│ ├── repositories/ # DB access layer
│ ├── schemas/ # Request/response schemas
│ ├── services/ # Business logic
│ └── utils.py # Utilities
├── alembic/ # Alembic migration environment
├── Dockerfile # Docker image definition
├── docker-compose.yaml # Service orchestration (PostgreSQL, API)
├── pyproject.toml # Project metadata and dependencies
├── requirements.txt # Pinned package versions
├── render.yaml # Deployment config for Render
└── start.sh # Startup script
```

---

## 🚀 Features

- 🔐 JWT-based authentication (`python-jose`, `passlib`)
- 📋 Manage customers, employees, work orders, and invoices
- 📄 Generate Word (.docx) invoices via `docxtpl`
- 🗃️ PostgreSQL + SQLAlchemy ORM + Alembic for
- ⚡ FastAPI async support
- ☁️ Google Drive integration via `aiogoogle`
- 🐳 Docker & Docker Compose support
- 🧪 Clean architecture with service, repository, and schema layers
- 🔍 Code linting with `ruff`

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mandacode/reinigungsservice-backend.git
cd reinigungsservice-backend
```

### 2. Create .env file
Create a .env file in the root directory with necessary environment variables, e.g.:
```plaintext
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/reinigungsservice
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
GOOGLE_DRIVE_CREDENTIALS_JSON=your_google_drive_credentials_json
SEED_FILE_ID=your_seed_file_id
```

### 3. Convert Google API credentials JSON to base64
You can use the following command to convert your Google API credentials JSON file to base64:
```bash
make encode-creds FILE=path/to/your/google_credentials.json
```
Then copy the content of `google_credentials_base64.txt` into your `.env` file as `GOOGLE_DRIVE_CREDENTIALS_JSON`.

### 4.  Run with Docker
```bash
make up
```

### 5. Run migrations
```bash
make migrate
```

## 📬 API Documentation
Once running, access interactive docs:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Running Tests
To run tests, use the following command:
```bash
make test
```
