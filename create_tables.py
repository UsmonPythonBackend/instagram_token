from models import User, Post, Comments, Messages, Likes, Followers, Tags, PostTags
from database import ENGINE, Base

Base.metadata.create_all(bind=ENGINE)