from cassandra.query import SimpleStatement

from dal.repositories.Repository import Repository
from dal.models.User import User


def parse_users(rows):
    users = []

    for row in rows:
        users.append(User(
            login=row.login,
            role=row.role_name,
            password=row.password_hash,
            registration_date=row.registration_date
        ))

    return users


class UserRepository(Repository):
    def __init__(self):
        Repository.__init__(self)

    def get_all_users(self):
        get_all_users_query = SimpleStatement(
            """
            SELECT login, role_name, password_hash, registration_date 
            FROM "LectureBotDBIS"."UserLectures";
            """,
            consistency_level=self.consistency_level)

        rows = self.session.execute(get_all_users_query)

        return parse_users(rows)

    def get_user_by_key(self, login):
        get_user_by_key_query = SimpleStatement(
            """
            SELECT login, role_name, password_hash, registration_date 
            FROM "LectureBotDBIS"."UserLectures"
            WHERE login = %s;
            """,
            consistency_level=self.consistency_level)

        rows = self.session.execute(
            get_user_by_key_query,
            [login]
        )

        return parse_users(rows)

    def insert_user(self, user):
        insert_resource_query = SimpleStatement(
            """
            INSERT INTO "LectureBotDBIS"."UserLectures"
            (login, role_name, password_hash, registration_date)
            VALUES
            (%s, %s, %s, %s);
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            insert_resource_query,
            (user.Login,
             user.Role,
             user.Password,
             user.RegistrationDate))

    def update_user_fields(self, user):
        update_user_fields_query = SimpleStatement(
            """
            UPDATE "LectureBotDBIS"."UserLectures"
            SET role_name = %s, password_hash = %s, registration_date = %s
            WHERE login = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            update_user_fields_query,
            (user.Role,
             user.Password,
             user.RegistrationDate,
             user.Login))

    def delete_user_by_key(self, login):
        delete_user_by_key_query = SimpleStatement(
            """
            DELETE FROM "LectureBotDBIS"."UserLectures"
            WHERE login = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            delete_user_by_key_query,
            [login]
        )
