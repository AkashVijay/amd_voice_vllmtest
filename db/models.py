from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import declarative_base
import os


Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    published = Column(DateTime)
  #  topic = Column(String)
    source = Column(String)

# db_path = os.path.abspath("arxiv.db")
engine = create_engine("sqlite:///arxiv.db")


Base.metadata.create_all(engine)