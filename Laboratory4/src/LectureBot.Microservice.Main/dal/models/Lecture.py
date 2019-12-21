from sqlalchemy import Column, String, Integer, ForeignKey

from dal.dbcontext import ModelBase


class Lecture(ModelBase):
    __tablename__ = 'Lecture'

    Id = Column(Integer, primary_key=True)
    UserLogin = Column(String, ForeignKey('User.Login'))

    Header = Column(String, nullable=False)
    Content = Column(String, nullable=False)

    def __init__(self, header, content, userlogin):
        self.Header = header
        self.Content = content
        self.UserLogin = userlogin
