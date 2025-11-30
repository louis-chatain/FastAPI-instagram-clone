from typing import List
from pydantic import BaseModel
from datetime import date


class PostModel(BaseModel):  # data that we will demand/receive from the user
    image_url: str
    image_url_type: str
    caption: str

#--------------------------------------------------------------------------

class User(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True


class Comment(BaseModel):
    id: int
    text: str
    username: str

    class ConfigDict:
        from_attributes = True

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: date
    users_id: int
    users: User
    comments: List[Comment] = []

    
    class ConfigDict:
        from_attributes = True
