# models.py

# from hello import db
from sqlalchemy.sql import func

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from database import engine

Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now()) 
    user_id = Column(Integer) # get user_id => project.user.id
    # user_id = Column(Integer, ForeignKey('user.id')) # get user_id => project.user.id


    def __repr__(self):
        return f'<Project "{self.name}..">' 

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



Base.metadata.create_all(engine)
