from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.routes import token, users, tweets

app = FastAPI()
app.include_router(token.router)
app.include_router(users.router)
app.include_router(tweets.router)

FAVICON = FileResponse('resources/favicon.ico')


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FAVICON


@app.get("/")
def root():
    return {"Hello": "World"}
