from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.controllers import router
from db.tables import create_tables, run_mappers
from db.config import engine


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
    allow_origins=["*"],  # Adjust this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)
