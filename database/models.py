from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class DbUser(Base):
    __tablename__: str = "user"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    username: Column[str] = Column(String)
    email: Column[str] = Column(String) #TODO add a unique=True
    hashed_password: Column[str] = Column(String)

    posts = relationship( # variable "items" must be the same in schemas_user
        'DbPost',
        back_populates='users',
        cascade="all, delete-orphan",
        passive_deletes=False,
        ) 


class DbPost(Base):
    __tablename__: str = "post"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    image_url: Column[str] = Column(String)
    image_url_type: Column[str] = Column(String)
    caption: Column[str] = Column(String)

    timestamp: Column[date] = Column(Date)

    users_id: Column[int] = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    users = relationship('DbUser', back_populates='posts')

    comments = relationship(
        'DbComment',
        back_populates='post',
        cascade="all, delete-orphan",
        passive_deletes=False,
        )


class DbComment(Base):
    __tablename__: str = "comment"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    text: Column[str] = Column(String)
    timestamp: Column[date] = Column(Date)

    user_id: Column[int] = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    post_id: Column[int] = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'))
    post = relationship("DbPost", back_populates="comments")
