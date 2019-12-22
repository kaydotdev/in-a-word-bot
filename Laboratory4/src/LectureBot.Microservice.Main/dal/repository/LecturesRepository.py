from dal.repository.Repository import Repository
from dal.models.Lecture import Lecture


class LecturesRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine, Lecture)

    def get_amount_of_lectures_of_user(self, user_login):
        return self.DBEngine.execute(f'''
        SELECT COUNT(*) AS "Lectures" 
        FROM "Lecture"
        WHERE "UserLogin" = '{user_login}';
        ''')

    def get_lectures_of_user(self, user_login):
        return self.Session.query(Lecture).filter_by(UserLogin=user_login).all()

    def get_lecture_by_id(self, identity):
        return self.Session.query(Lecture).filter_by(Id=identity).first()

    def update_lecture(self, identity, entity):
        self.Session.query(Lecture).filter_by(Id=identity).update(self.map_entity(entity))

    def drop_lecture(self, identity):
        self.Session.query(Lecture).filter_by(Id=identity).delete()
