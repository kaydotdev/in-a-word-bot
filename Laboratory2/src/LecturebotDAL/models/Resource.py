from sqlalchemy import Column, String, Integer

from LecturebotDAL.dbcontext import ModelBase


class Resource(ModelBase):
    __tablename__ = 'Resource'

    URL = Column(String, primary_key=True)

    Description = Column(String, nullable=False)
    TimesVisited = Column(Integer, nullable=False)

    def __init__(self, url, description):
        self.URL = url
        self.Description = description
        self.TimesVisited = 1
