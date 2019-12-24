from dal.repository.Repository import Repository
from dal.models.Role import Role


class RoleRepository(Repository):
    def __init__(self, session, model_base, db_engine):
        Repository.__init__(self, session, model_base, db_engine, Role)

    def get_user_role(self, user_login):
        return self.DBEngine.execute(f'''
        SELECT "Role"."Name"
        FROM "Role" JOIN "User"
        ON "Role"."Id" = "User"."RoleId"
        WHERE "User"."Login" = '{user_login}';
        ''')
