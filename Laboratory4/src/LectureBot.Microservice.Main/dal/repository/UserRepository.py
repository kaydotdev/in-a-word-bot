from dal.repository.Repository import Repository
from dal.models.User import User


class UserRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine, User)

    def get_user_by_login(self, user_login):
        return self.Session.query(User).filter_by(Login=user_login).all()

    def get_total_amount_of_users(self):
        return self.DBEngine.execute(f'''
            SELECT COUNT(*) 
            FROM "User"
            ''')
