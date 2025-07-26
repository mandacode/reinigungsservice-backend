from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.database.orm import create_tables, run_mappers
from app.database.config import engine
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    await create_tables(engine=engine)
    run_mappers()
    yield
    print("Shutting down the application...")


app = FastAPI(lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_domain,],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)



