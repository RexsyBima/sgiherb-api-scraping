from sqlalchemy import Column, Integer, String, Float, Boolean
from db import Base, engine


class SgiherbSqlAlchemyItem(Base):
    __tablename__ = "items"

    no = Column(Integer, primary_key=True)
    id = Column(Integer)
    displayName = Column(String)
    isAvailableToPurchase = Column(Boolean)
    partNumber = Column(String)
    rootCategoryId = Column(Integer)
    rootCategoryName = Column(String)
    url = Column(String)
    urlName = Column(String)
    discountPrice = Column(Float)
    listPrice = Column(Float)
    brandCode = Column(String)
    brandName = Column(String)
    brandUrl = Column(String)
    primaryImageIndex = Column(Integer)


Base.metadata.create_all(engine)
