from sqlalchemy import Column, Integer, Float, DateTime, String

from address_book.database import Base

from datetime import datetime, timezone


class AddressBook(Base):
    """
    Table column details
    """
    __tablename__ = "address_book"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_email = Column(String(120), nullable=False)
    user_name = Column(String(200), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)