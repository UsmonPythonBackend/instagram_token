from pydantic import BaseModel
from typing import Optional, List, BinaryIO

class RegisterModel(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]

class Config:
    orm_mode = True
    schema_extra = {
        "username": "pipsudo",
        "password": "pipsudo123",
        "email": "pipsudo@gmail.com",
        "is_active": True,
        "is_staff": True

    }

class LoginModel(BaseModel):
    username: Optional[str]
    password: Optional[str]

# class PasswordReset(BaseModel):
#     pass

class CreatePost(BaseModel):
    image_path: Optional[str]
    caption: Optional[str]


class UserModel(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    bio: Optional[str]
    profile_picture: Optional[str]
    is_active: Optional[bool]
    is_staff: Optional[bool]



class PostListModel(BaseModel):
    id: Optional[int]
    image_path: Optional[str]
    caption: Optional[str]


class SettingsModel(BaseModel):
    authjwt_secret_key: str = "d10c3a133738c586521b7695c5d4819f4bf790b8596d6a760293523ed9429a87"


class PostUpdateModel(BaseModel):
    user_id: Optional[int]
    image_path: Optional[str]
    caption: Optional[str]



class CommentsListModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    post_id: Optional[int]
    status: Optional[bool]


class CommentsCreateModel(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    status: Optional[bool]


class CommentsUpdateModel(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    status: Optional[bool]



class LikesListModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    post_id: Optional[int]
    status: Optional[bool]


class LikesCreateModel(BaseModel):
    user_id: Optional[int]
    post_id: Optional[int]
    status: Optional[bool]



class FollowsListModel(BaseModel):
    id: Optional[int]
    follower_id: Optional[int]
    following_id: Optional[int]


class FollowsCreateModel(BaseModel):
    follower_id: Optional[int]
    following_id: Optional[int]



class TagsListModel(BaseModel):
    id: Optional[int]
    tag_name: Optional[str]


class TagsCreateModel(BaseModel):
    tag_name: Optional[str]



class StoriesListModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    image_url: Optional[str]
    caption: Optional[str]


class StoriesCreateModel(BaseModel):
    user_id: Optional[int]
    image_url: Optional[str]
    caption: Optional[str]

#
# class UserPasswordResetModel(BaseModel):
#     password: Optional[str]
#     password_2: Optional[str]
#
