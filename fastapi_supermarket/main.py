from fastapi import FastAPI

from fastapi_supermarket.controllers import auth_controller, users_controller

app = FastAPI()

app.include_router(auth_controller.router, prefix='/auth', tags=['Auth'])
app.include_router(users_controller.router, tags=['Users'])
