from contextlib import asynccontextmanager
import logging
import sys

from fastapi import FastAPI

from api.core.config import app_config
from api.database.session import db_session_manager
from api.routers import auth_router, customers_router, users_router


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if app_config.log_level == "DEBUG" else logging.INFO,
    format="%(levelname)s:     %(message)s",
)

logger = logging.getLogger(__name__)
logger.info("API is initializing")
logger.info("Log level is %s", app_config.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if db_session_manager.engine is not None:
        await db_session_manager.close()


app = FastAPI(
    lifespan=lifespan,
    debug=True if app_config.log_level == "DEBUG" else False,
    title="Project Assignment Portal",
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(customers_router.router)


# TO DELETE
@app.get("/api/python")
async def hello_world():
    return {"message": "Hello World"}
