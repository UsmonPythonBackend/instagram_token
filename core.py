from fastapi import FastAPI
from routers.auth import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import SettingsModel
from routers.posts import post_router

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return SettingsModel()

app.include_router(auth_router)
app.include_router(post_router)


@app.get("/")
def root():
    return {"msg": "welcome"}