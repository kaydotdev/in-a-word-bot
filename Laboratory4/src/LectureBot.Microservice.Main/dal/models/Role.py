from sqlalchemy import Column, String, Integer

from dal.dbcontext import ModelBase


class Role(ModelBase):
    __tablename__ = 'Role'

    Id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Priority = Column(String, nullable=False)

    def __init__(self, name, priority):
        self.Name = name
        self.Priority = priority


