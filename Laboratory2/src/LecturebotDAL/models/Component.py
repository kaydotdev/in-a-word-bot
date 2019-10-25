from sqlalchemy import Column, String, Integer, ForeignKey

from LecturebotDAL.dbcontext import ModelBase


class Component(ModelBase):
    __tablename__ = 'Component'

    Id = Column(Integer, primary_key=True)
    ResourceURL = Column(String, ForeignKey('Resource.URL'))

    Tag = Column(String, nullable=False)
    Inner = Column(String, nullable=True)

    def __init__(self, tag, inner, resourceurl):
        self.Tag = tag
        self.Inner = inner
        self.ResourceURL = resourceurl
