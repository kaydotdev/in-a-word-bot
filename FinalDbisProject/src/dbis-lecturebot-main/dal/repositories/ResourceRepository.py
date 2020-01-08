from cassandra.query import SimpleStatement

from dal.repositories.Repository import Repository
from dal.models.Resource import Resource


def parse_resources(rows):
    resources = []

    for row in rows:
        resources.append(Resource(
            user_login=row.login,
            url=row.url,
            creation_date=row.creation_date,
            description=row.description,
            times_visited=row.times_visited
        ))

    return resources


class ResourceRepository(Repository):
    def __init__(self):
        Repository.__init__(self)

    def get_all_resources(self):
        get_all_resources_query = SimpleStatement(
            """
            SELECT login, url, creation_date, description, times_visited 
            FROM "LectureBotDBIS"."Resources";
            """,
            consistency_level=self.consistency_level)

        rows = self.session.execute(get_all_resources_query)

        return parse_resources(rows)

    def get_resources_by_keys(self, login, url):
        get_resources_by_keys_query = SimpleStatement(
            """
            SELECT login, url, creation_date, description, times_visited 
            FROM "LectureBotDBIS"."Resources"
            WHERE login = %s AND url = %s;
            """,
            consistency_level=self.consistency_level)

        rows = self.session.execute(
            get_resources_by_keys_query,
            (login, url)
        )

        return parse_resources(rows)

    def get_resources_by_foreign_key(self, login):
        get_resources_by_foreign_key_query = SimpleStatement(
            """
            SELECT login, url, creation_date, description, times_visited 
            FROM "LectureBotDBIS"."Resources"
            WHERE login = %s;
            """,
            consistency_level=self.consistency_level)

        rows = self.session.execute(
            get_resources_by_foreign_key_query,
            [login]
        )

        resources = parse_resources(rows)

        if len(resources) == 1:
            if resources[0].URL is None:
                return []
            else:
                return resources
        else:
            return resources

    def insert_resource(self, resource):
        insert_resource_query = SimpleStatement(
            """
            INSERT INTO "LectureBotDBIS"."Resources"
            (login, url, creation_date, description, times_visited)
            VALUES
            (%s, %s, %s, %s, %s);
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            insert_resource_query,
            (resource.User_Login,
             resource.URL,
             resource.Creation_Date,
             resource.Description,
             resource.TimesVisited))

    def update_resource_fields(self, resource):
        update_resource_fields_query = SimpleStatement(
            """
            UPDATE "LectureBotDBIS"."Resources"
            SET creation_date = %s, description = %s, times_visited = %s
            WHERE login = %s AND url = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            update_resource_fields_query,
            (resource.User_Login,
             resource.URL,
             resource.Creation_Date,
             resource.Description,
             resource.TimesVisited))

    def delete_resource_by_keys(self, login, url):
        delete_lecture_by_keys_query = SimpleStatement(
            """
            DELETE FROM "LectureBotDBIS"."Resources"
            WHERE login = %s, url = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            delete_lecture_by_keys_query,
            (login, url)
        )
