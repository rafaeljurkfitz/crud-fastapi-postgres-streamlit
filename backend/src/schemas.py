from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, PositiveFloat, field_validator


class CategoryBase(Enum):
    category1 = "Eletrônico"
    category2 = "Eletrodoméstico"
    category3 = "Móveis"
    category4 = "Roupas"
    category5 = "Calçados"


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    category: str
    email_provider: EmailStr

    @field_validator("category")
    def check_categoria(cls, v):
        if v in [item.value for item in CategoryBase]:
            return v
        raise ValueError("Categoria inválida")


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    category: Optional[str] = None
    email_provider: Optional[EmailStr] = None

    @field_validator("category", mode="before")
    def check_categoria(cls, v):
        if v is None:
            return v
        if v in [item.value for item in CategoryBase]:
            return v
        raise ValueError("Categoria inválida")


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    products_: list[ProductBase] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None
