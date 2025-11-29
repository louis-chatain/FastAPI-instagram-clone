from pydantic import BaseModel


class UserModel(BaseModel):  # data that we will demand/receive from the user
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True
