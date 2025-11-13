import uvicorn
import os
from redis import Redis

from fastapi import FastAPI
from app.api.routes import district, courier, order, user

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_user = os.getenv("REDIS_USER", None)
redis_password = os.getenv("REDIS_PASSWORD", None)

redis_client = Redis(host=redis_host, port=redis_port, password=redis_password)


app = FastAPI(
    title="Сервис распределения заказов по курьерам"
)
@app.get('/')
async def root():
    return {'message': 'Order courier service'}


app.include_router(district.router)
app.include_router(courier.router)
app.include_router(order.router)
app.include_router(user.router)


if __name__ == '__main__':
    uvicorn.run("main:proj_app", host="0.0.0.0", port=8000, reload=True)
