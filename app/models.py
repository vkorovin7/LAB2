from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    description = Column(String)
    
    # Важно: определение relationship
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    # Важно: ForeignKey должен ссылаться на правильную таблицу и поле
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Важно: определение relationship
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=False, default="pending")
    
    # Важно: определение relationships
    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    product = relationship("Product", back_populates="orders")