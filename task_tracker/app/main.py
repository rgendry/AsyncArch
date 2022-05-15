from fastapi import FastAPI

from app.config import settings
from app.api import tasks


def get_app() -> FastAPI:
    application = FastAPI(title=settings.SERVICE_NAME, root_path=settings.ROOT_PATH, debug=settings.DEBUG)
    application.include_router(tasks.router, prefix="/tasks")
    return application


app = get_app()
