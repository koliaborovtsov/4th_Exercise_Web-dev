from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .seed_data import seed_products
from .routers import products, orders

app = FastAPI(
    title="LampStore API",
    description="API для интернет-магазина ламп",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():
    """
    Инициализация базы данных и заполнение тестовыми данными при запуске
    """
    print("Запуск LampStore API...")
    init_db()
    print("База данных инициализирована")
    seed_products()
    print("Запуск завершен!")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "LampStore API работает", "version": "1.0.0"}


@app.get("/api")
async def root():
    return {
        "name": "LampStore API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "products": "/api/products",
            "orders": "/api/orders",
            "health": "/api/health",
        },
    }
