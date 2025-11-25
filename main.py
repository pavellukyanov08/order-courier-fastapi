import uvicorn
import os
from redis import Redis

from fastapi import FastAPI
from app.api.users.controllers import router as user_router
from app.api.couriers.controllers import router as courier_router
from app.utils.logger import LoggerMiddleware

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_user = os.getenv("REDIS_USER", None)
redis_password = os.getenv("REDIS_PASSWORD", None)

redis_client = Redis(host=redis_host, port=redis_port, password=redis_password)


app = FastAPI(
    title="Сервис распределения заказов по курьерам"
)


# app.include_router(district.router)
app.include_router(courier_router)
# app.include_router(order.router)
app.include_router(user_router)
app.add_middleware(LoggerMiddleware)

if __name__ == '__main__':
    uvicorn.run("main:proj_app", host="0.0.0.0", port=8000, reload=True)
