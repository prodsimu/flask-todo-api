from typing import Optional

from pydantic import BaseModel, Field


class RegisterBody(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8, max_length=64)


class LoginBody(BaseModel):
    username: str
    password: str


class UpdatePasswordBody(BaseModel):
    password: str = Field(min_length=8, max_length=64)


class UpdateUserBody(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=64)
    role: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    role: str

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    id: int
    username: str
    role: str
    token: str


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int


class UserListResponse(BaseModel):
    data: list[UserResponse]
    pagination: PaginationMeta
