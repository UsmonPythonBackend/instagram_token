from fastapi import APIRouter, status, Depends, HTTPException
from models import Post, User
from database import ENGINE, Session
from fastapi.encoders import jsonable_encoder
from schemas import CreatePost, PostUpdateModel
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)


post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.get("/")
async def get_posts(Authorization: AuthJWT = Depends(AuthJWT)):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        posts = session.query(Post).filter(Post.user == current_user).all()
        return jsonable_encoder(posts)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")


@post_router.post("/")
async def create_post(post: CreatePost, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            new_post = Post(
                user_id=check_user.id,
                caption=post.caption,
                image_path=post.image_path
            )
            session.add(new_post)
            session.commit()
            data = {
                "success": True,
                "code": 201,
                "message": "Created post successfully"
            }
            return jsonable_encoder(data)
        return {"success": False, "code": 400, "message": "Bad Request"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid")





@post_router.put("/{id}")
async def update_post(id: int, post: PostUpdateModel, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            check_post = session.query(Post).filter(Post.id == id).first()
            if check_post:
                for key, value in post.dict().items():
                    setattr(check_post, key, value)

                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Successfully updated post",
                        "object": {
                            "caption": check_post.caption,
                            "user_id": check_post.id,
                            "image_path": check_post.image_path,
                        }
                    }
                    session.add(check_post)
                    session.commit()
                    return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@post_router.delete("/{id}")
async def delete_post(id: int, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            post = session.query(Post).filter(Post.id == id).first()
            if post:
                session.delete(post)
                session.commit()
                return jsonable_encoder({"code": 200, "message": "Successfully deleted post"})
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')