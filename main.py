from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI

from routes.auth import router as AuthRouter
from routes.author import (
    public_router as AuthorRouter,
    admin_router as AuthorRouterAdmin,
)
from routes.book import (
    public_router as BookRouter,
    admin_router as BookRouterAdmin,
)
from routes.user import router as UserRouter

from core.config import Settings, get_settings
from core.db import create_db_and_tables


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield
    print("APP is shutdown")


app = FastAPI(
    title=settings.api_title,
    lifespan=lifespan,
    version=settings.api_version,
    description="Book Store API to handle payment etc",
)


@app.get("/", include_in_schema=False)
def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"Name": settings.api_title, "API Version": settings.api_version}


app.include_router(AuthRouter)
app.include_router(AuthorRouterAdmin)
app.include_router(BookRouterAdmin)
app.include_router(AuthorRouter)
app.include_router(BookRouter)
app.include_router(UserRouter)
