from sqlalchemy import Column, String, Integer, ForeignKey

from LecturebotDAL.dbcontext import ModelBase


class Attribute(ModelBase):
    __tablename__ = 'Attribute'

    Id = Column(Integer, primary_key=True)
    ComponentId = Column(Integer, ForeignKey('Component.Id'))

    Key = Column(String, nullable=False)
    Value = Column(String, nullable=False)

    def __init__(self, key, value, componentid):
        self.Key = key
        self.Value = value
        self.ComponentId = componentid
