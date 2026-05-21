from datetime import datetime
# EmailStr is a special type provided by Pydantic that validates that the input is a valid email address. It ensures that any value assigned to an EmailStr field conforms to the standard email format, which includes an "@" symbol and a domain name. This helps prevent invalid email addresses from being accepted in the application.
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass

# ConfigDict(from_attributes=True) allows Pydantic to create a UserResponse model from the attributes of the User SQLAlchemy model. This means that when we return a UserResponse, Pydantic will automatically populate its fields based on the corresponding attributes of the User model instance.
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None
    image_path: str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int  # TEMPORARY


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse