from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )

# One-to-many relationship: A user can have multiple posts, but each post belongs to one user.
# The `cascade="all, delete-orphan"` option ensures that when a user is deleted, all their associated posts are also deleted.
    posts: Mapped[list[Post]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

# The `image_path` property is a computed attribute that generates the URL path for the user's profile picture based on the `image_file` field. If `image_file` is not set, it returns a default image path.
# This allows the application to easily access the correct image path for a user's profile picture without needing to store the full path in the database.
    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

# The `back_populates` parameter is used to establish a bidirectional relationship between the `User` and `Post` models. It allows us to access the related posts from a user instance and the related user from a post instance.
    author: Mapped[User] = relationship(back_populates="posts")