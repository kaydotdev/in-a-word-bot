from sqlalchemy import Column, String, Integer, Date, ForeignKey

from dal.dbcontext import ModelBase


class User(ModelBase):
    __tablename__ = 'User'

    Login = Column(String, primary_key=True)
    RoleId = Column(Integer, ForeignKey('Role.Id'))

    PasswordHash = Column(String, nullable=False)
    RegistrationDate = Column(Date, nullable=False)

    def __init__(self, login, password, regdate, roleid):
        self.Login = login
        self.PasswordHash = password
        self.RegistrationDate = regdate

        self.RoleId = roleid
