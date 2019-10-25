from sqlalchemy import Column, String, Integer

from LecturebotDAL.dbcontext import ModelBase


class Role(ModelBase):
    __tablename__ = 'Role'

    Id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Priority = Column(String, nullable=False)

    def __init__(self, identity, name, priority):
        self.Id = identity
        self.Name = name
        self.Priority = priority


