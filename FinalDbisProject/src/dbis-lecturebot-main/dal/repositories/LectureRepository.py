from cassandra.query import SimpleStatement

from dal.repositories.Repository import Repository
from dal.models.Lecture import Lecture


def parse_lectures(rows):
    lectures = []

    for row in rows:
        lectures.append(Lecture(
            user_login=row.login,
            header=row.lecture_header,
            content=row.lecture_content,
            status=row.lecture_status,
            creation_date=row.lecture_creation_date
        ))

    return lectures


class LecturesRepository(Repository):
    def __init__(self):
        Repository.__init__(self)

    def get_all_lectures(self):
        get_all_lectures_query = SimpleStatement(
            """
            SELECT lecture_header, lecture_content, lecture_status, lecture_creation_date, login 
            FROM "LectureBotDBIS"."UserLectures";
            """,
            consistency_level=self.consistency_level)
        rows = self.session.execute(get_all_lectures_query)

        return parse_lectures(rows)

    def get_lectures_by_keys(self, login, header):
        get_lectures_by_keys_query = SimpleStatement(
            """
            SELECT lecture_header, lecture_content, lecture_status, lecture_creation_date, login 
            FROM "LectureBotDBIS"."UserLectures"
            WHERE login = %s AND lecture_header = %s;
            """,
            consistency_level=self.consistency_level)
        rows = self.session.execute(
            get_lectures_by_keys_query,
            (login, header)
        )

        return parse_lectures(rows)

    def get_lectures_by_foreign_key(self, login):
        get_lectures_by_foreign_key_query = SimpleStatement(
            """
            SELECT lecture_header, lecture_content, lecture_status, lecture_creation_date, login 
            FROM "LectureBotDBIS"."UserLectures"
            WHERE login = %s;
            """,
            consistency_level=self.consistency_level)
        rows = self.session.execute(
            get_lectures_by_foreign_key_query,
            [login]
        )

        lectures = parse_lectures(rows)

        if len(lectures) == 1:
            if lectures[0].Header is None:
                return []
            else:
                return lectures
        else:
            return lectures

    def insert_lecture(self, lecture):
        insert_lecture_query = SimpleStatement(
            """
            INSERT INTO "LectureBotDBIS"."UserLectures"
            (login, lecture_header, lecture_status, lecture_content, lecture_creation_date)
            VALUES
            (%s, %s, %s, %s, %s);
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            insert_lecture_query,
            (lecture.User_Login,
             lecture.Header,
             lecture.Status,
             lecture.Content,
             lecture.Creation_Date))

    def update_lecture_fields(self, lecture):
        update_lecture_fields_query = SimpleStatement(
            """
            UPDATE "LectureBotDBIS"."UserLectures"
            SET lecture_content = %s, lecture_status = %s, lecture_creation_date = %s
            WHERE login = %s AND lecture_header = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            update_lecture_fields_query,
            (lecture.Content,
             lecture.Status,
             lecture.Creation_Date,
             lecture.User_Login,
             lecture.Header))

    def delete_lecture_by_keys(self, login, header):
        delete_lecture_by_keys_query = SimpleStatement(
            """
            DELETE FROM "LectureBotDBIS"."UserLectures"
            WHERE login = %s AND lecture_header = %s;
            """,
            consistency_level=self.consistency_level)

        self.session.execute(
            delete_lecture_by_keys_query,
            (login,
             header))
