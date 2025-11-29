from pydantic import BaseModel
from datetime import date

class PostModel(BaseModel):  # data that we will demand/receive from the user
    image_url: str
    image_url_type: str
    caption: str


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: date

    class ConfigDict:
        from_attributes = True
