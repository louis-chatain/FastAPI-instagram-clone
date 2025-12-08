from datetime import date
from typing import List
from pydantic import BaseModel


class UserModel(BaseModel):  # data that we will demand/receive from the front-end guy/user
    username: str
    email: str
    password: str

#--------------------------------------------------------------------------

class Post(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: date
    
    class ConfigDict:
        from_attributes = True

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    posts: List[Post] = []  #the variable "items" is named so because it is also the name of the relationship in the db model User (MUST be the same!)

    class ConfigDict:
        from_attributes = True
