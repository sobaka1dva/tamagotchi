from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///tamagotchi.db', echo=True)


class Tamagotchi(Base):
    __tablename__ = 'tamagotchi'
    id = Column(Integer, primary_key=True)
    name = Column(String, default="John")
    max_health = Column(Integer, default=20)
    current_health = Column(Integer, default=20)
    image_path = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
