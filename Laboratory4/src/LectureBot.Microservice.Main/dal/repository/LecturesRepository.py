from dal.repository.Repository import Repository
from dal.models.Lecture import Lecture


class LecturesRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine)

    def get_amount_of_lectures_of_user(self, user_login):
        return self.DBEngine.execute(f'''
        SELECT COUNT("ResourceURL") FROM "UserHasResources"
        WHERE "UserLogin" = '{user_login};
        ''')

    def get_lectures_of_user(self, user_login):
        return self.Session.query(Lecture).filter_by(UserLogin=user_login).all()
