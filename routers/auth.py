from fastapi import APIRouter, HTTPException, status, Depends
import datetime
from database import Session, ENGINE
from models import User
from schemas import RegisterModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.get("/")
async def auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        return {"message": "auth page"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid")

@auth_router.post("/login")
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user:
        if check_password_hash(check_user.password, user.password):

            access_token = Authorize.create_access_token(subject=user.username, expires_time=datetime.timedelta(hours=3))
            refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=datetime.timedelta(days=7))
            data = {
                "success": True,
                "code": 200,
                "message": "Login Successful",
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }
            return jsonable_encoder(data)

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

@auth_router.post("/register")
async def register(user: RegisterModel):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "message": "User created successfully",
        "object": {
            "username": user.username,
            "email": user.email,
            "password": generate_password_hash(user.password)
        }
    }
    return jsonable_encoder(data)

@auth_router.get("/users")
async def users(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        users = session.query(User).all()
        return jsonable_encoder(users)

    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid")
