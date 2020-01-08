from bll.dto.LectureDTO import LectureDTO

from dal.models.Lecture import Lecture
from dal.repositories.LectureRepository import LecturesRepository


# noinspection PyBroadException
class LecturesService:
    def __init__(self):
        self.lecture_repository = LecturesRepository()

    def get_all_user_lectures(self, login):
        lectures = self.lecture_repository.get_lectures_by_foreign_key(login)
        mapped_lectures = [LectureDTO(
            header=lecture.Header,
            content=lecture.Content,
            status=lecture.Status,
            creation_date=lecture.Creation_Date
        ) for lecture in lectures]

        return mapped_lectures

    def get_lecture_by_login_and_header(self, login, header):
        lectures = self.lecture_repository.get_lectures_by_keys(login, header)
        mapped_lectures = [LectureDTO(
            header=lecture.Header,
            content=lecture.Content,
            status=lecture.Status,
            creation_date=lecture.Creation_Date
        ) for lecture in lectures]

        return mapped_lectures

    def get_count_of_user_lectures(self, login):
        lectures = self.get_all_user_lectures(login)
        return len(lectures)

    def add_lecture(self, login, new_lecture):
        lecture = self.lecture_repository.get_lectures_by_keys(login, new_lecture.Header)

        if len(lecture) != 0:
            return "Lecture with this header already exists!", 400
        else:
            lecture_to_insert = Lecture(
                user_login=login,
                header=new_lecture.Header,
                content=new_lecture.Content,
                status=new_lecture.Status,
                creation_date=new_lecture.Creation_Date
            )
            try:
                self.lecture_repository.insert_lecture(lecture_to_insert)
                return "Lecture was successfully added!", 200
            except Exception:
                return "Oops, something went wrong!", 500

    def edit_lecture(self, login, old_lecture_header, new_lecture):
        lectures = self.lecture_repository.get_lectures_by_keys(login, old_lecture_header)

        if len(lectures) == 0:
            return "This lecture doesn't exist!", 400
        else:
            try:
                if old_lecture_header != new_lecture.Header:
                    self.lecture_repository.delete_lecture_by_keys(login, old_lecture_header)

                    lecture_to_insert = Lecture(
                        user_login=login,
                        header=new_lecture.Header,
                        content=new_lecture.Content,
                        status=new_lecture.Status,
                        creation_date=new_lecture.Creation_Date
                    )

                    self.lecture_repository.insert_lecture(lecture_to_insert)
                    return "Lecture was successfully edited!", 200
                else:
                    lecture_to_update = Lecture(
                        user_login=login,
                        header=new_lecture.Header,
                        content=new_lecture.Content,
                        status=new_lecture.Status,
                        creation_date=new_lecture.Creation_Date
                    )

                    self.lecture_repository.update_lecture_fields(lecture_to_update)
                    return "Lecture was successfully edited!", 200
            except Exception:
                return "Oops, something went wrong!", 500

    def delete_lecture(self, user, lecture):
        self.lecture_repository.delete_lecture_by_keys(user.Login, lecture.Header)
