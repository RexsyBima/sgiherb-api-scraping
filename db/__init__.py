from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///sgiherb-api.db")
Session = sessionmaker(bind=engine)
session = Session()
