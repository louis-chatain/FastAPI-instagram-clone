from pydantic import BaseModel
from datetime import date

class CommentModel(BaseModel):  # data that we will demand/receive from the user
    text: str
    username: str


class CommentDisplay(BaseModel):
    id: int
    text: str
    username: str
    timestamp: date

    class ConfigDict:
        from_attributes = True
