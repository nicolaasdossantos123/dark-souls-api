from fastapi import FastAPI

import models
from routes import router

app = FastAPI()

app.include_router(router)