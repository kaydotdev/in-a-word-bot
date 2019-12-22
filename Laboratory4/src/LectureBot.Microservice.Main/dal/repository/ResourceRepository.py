from dal.repository.Repository import Repository
from dal.models.Resource import Resource


class ResourceRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine, Resource)

    def get_amount_of_resources_of_user(self, user_login):
        return self.DBEngine.execute(f'''
                SELECT COUNT("UserHasResources"."ResourceURL") AS "URLS"
                FROM "UserHasResources"
                JOIN "User" ON "User"."Login" = "UserHasResources"."UserLogin"
                WHERE "User"."Login" = '{user_login}';
                ''')
