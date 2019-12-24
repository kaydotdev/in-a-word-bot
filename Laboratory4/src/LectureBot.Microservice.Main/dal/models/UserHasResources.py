from sqlalchemy import Column, String, ForeignKey

from dal.dbcontext import ModelBase


class UserHasResources(ModelBase):
    __tablename__ = 'UserHasResources'

    UserLogin = Column(String, ForeignKey('User.Login'), primary_key=True)
    ResourceURL = Column(String, ForeignKey('Resource.URL'), primary_key=True)

    def __init__(self, userlogin, resourceurl):
        self.UserLogin = userlogin
        self.ResourceURL = resourceurl
