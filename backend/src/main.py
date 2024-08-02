import time

import models
from database import engine
from fastapi import FastAPI, Request
from routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(router)
