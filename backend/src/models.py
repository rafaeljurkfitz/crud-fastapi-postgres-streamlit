from database import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ProductModel(Base):
    __tablename__ = "products"  # esse será o nome da tabela

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    category = Column(String, index=True)
    email_provider = Column(String, index=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), index=True)

    owner = relationship("User", back_populates="products_")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    products_ = relationship("ProductModel", back_populates="owner")
