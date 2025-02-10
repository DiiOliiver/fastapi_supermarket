from fastapi import FastAPI

from fastapi_supermarket.controllers import users_controller

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


app.include_router(users_controller.router, tags=['Users'])
