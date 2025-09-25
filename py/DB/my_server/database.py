from my_server import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    image: Mapped[str] = mapped_column(default="default_profile.jpg")
    posts = relationship("Posts", back_populates="user")

class Posts(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    time: Mapped[int]  # UNIX
    title: Mapped[str]
    content: Mapped[str]
    user = relationship("User", back_populates="posts") 