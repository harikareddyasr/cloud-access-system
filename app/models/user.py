from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="customer")  # 'admin' or 'customer'
    subscriptions = relationship("Subscription", back_populates="user")

