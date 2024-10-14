from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    is_completed = Column(Boolean, default=False)

engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(engine)
