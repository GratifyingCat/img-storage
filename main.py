import uvicorn

from fastapi import FastAPI

from images.routers import router as images_router

from accounts.routers import router as accounts_router

from database import database


database.create_tables()

app = FastAPI()

app.include_router(images_router)
app.include_router(accounts_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    