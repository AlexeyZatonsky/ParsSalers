from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String, DOUBLE, DateTime, ForeignKey


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Shops(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    catigory = Column(String)

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(DOUBLE)
    data = Column(DateTime, default=datetime.utcnow)
    search_query = Column(String, nullable=True)
    shop_id = Column(Integer, ForeignKey(Shops.id))

