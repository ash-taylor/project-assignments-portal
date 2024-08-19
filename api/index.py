from fastapi import FastAPI

from api.routers import users


app = FastAPI()

app.include_router(users.router)


@app.get("/api/python")
async def hello_world():
    return {"message": "Hello World"}
