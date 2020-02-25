from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        String,
                        Sequence,
                        Integer,
                        Float,
                        Date)


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(Date(), nullable=False)
    updated_at = Column(Date())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(Date(), nullable=False)
    updated_at = Column(Date())
