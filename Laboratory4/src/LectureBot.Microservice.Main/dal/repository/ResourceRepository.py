from dal.repository.Repository import Repository
from dal.models.Resource import Resource


class ResourceRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine, Resource)

    def drop_user_and_resource_relation(self, user_login, resource_url):
        self.DBEngine.execute(f'''
                DELETE FROM "UserHasResources"
                WHERE "UserLogin" = '{user_login}' 
                AND "ResourceURL" = '{resource_url}';
                ''')

    def insert_user_and_resource_relation(self, user_login, resource_url):
        self.DBEngine.execute(f'''
                INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
                VALUES ('{user_login}', '{resource_url}');
                ''')

    def get_amount_of_resources_of_user(self, user_login):
        return self.DBEngine.execute(f'''
                SELECT COUNT("UserHasResources"."ResourceURL") AS "URLS"
                FROM "UserHasResources"
                JOIN "User" ON "User"."Login" = "UserHasResources"."UserLogin"
                WHERE "User"."Login" = '{user_login}';
                ''')

    def get_by_url(self, url):
        return self.Session.query(Resource).filter_by(URL=url).first()

    def get_resources_of_user(self, user_login):
        return self.DBEngine.execute(f'''
                SELECT "Resource"."URL", "Resource"."Description", "Resource"."TimesVisited" FROM "Resource"
                JOIN "UserHasResources" ON "UserHasResources"."ResourceURL" = "Resource"."URL"
                JOIN "User" ON "UserHasResources"."UserLogin" = "User"."Login"
                WHERE "User"."Login" = '{user_login}'
                ORDER BY "Resource"."TimesVisited" DESC;
                ''')

    def update_resource(self, url, entity):
        self.Session.query(Resource).filter_by(URL=url).update(self.map_entity(entity))

    def drop_resource(self, url):
        self.Session.query(Resource).filter_by(URL=url).delete()
