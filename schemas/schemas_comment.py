from pydantic import BaseModel
from datetime import date

class CommentModel(BaseModel):  # data that we will demand/receive from the user
    text: str
    post_id: int

#--------------------------------------------------------------------------

class Post(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: date
    users_id: int
    class ConfigDict:
        from_attributes = True

class CommentDisplay(BaseModel):
    id: int
    text: str
    username: str 
    timestamp: date
    post_id : int
    post : Post

    class ConfigDict:
        from_attributes = True
