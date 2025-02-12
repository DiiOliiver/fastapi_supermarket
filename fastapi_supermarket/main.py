from fastapi import FastAPI

from fastapi_supermarket.controllers import (
    auth_controller,
    category_controller,
    product_controller,
    sales_controller,
    users_controller,
)

app = FastAPI()

app.include_router(auth_controller.router)
app.include_router(users_controller.router)
app.include_router(category_controller.router)
app.include_router(product_controller.router)
app.include_router(sales_controller.router)
