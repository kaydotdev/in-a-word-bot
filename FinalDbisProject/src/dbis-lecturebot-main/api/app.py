from flask import Flask, make_response, request

import datetime
import json

from dal.repositories.LectureRepository import LecturesRepository
from dal.models.Lecture import Lecture

from api.settings.apisettings import API_SECRET

from bll.services.UserService import UserService
from bll.dto.UserDTO import UserDTO


def date_converter(o):
    if isinstance(o, datetime.date):
        return datetime.datetime.combine(o, datetime.datetime.min.time()).strftime("%Y-%m-%d")


def serialize(obj):
    return json.dumps(obj.__dict__, default=date_converter)


def serialize_array(arr):
    return '\n'.join([serialize(element) for element in arr])


app = Flask(__name__)
app.secret_key = API_SECRET

user_service = UserService(API_SECRET)


@app.route('/api/lecture', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_lecture():
    lecture_repository = LecturesRepository()

    if request.method == 'GET':
        lectures = lecture_repository.get_all_lectures()
        return serialize_array(lectures), 200
    elif request.method == 'POST':
        lecture = Lecture(
            user_login=str(request.json['user_login']),
            header=str(request.json['header']),
            content=str(request.json['content']),
            status=str(request.json['status']),
            creation_date=str(request.json['creation_date'])
        )
        lecture_repository.insert_lecture(lecture)
        response = make_response("Lecture was successfully added!")
        return response, 200
    elif request.method == 'PUT':
        lecture = Lecture(
            user_login=str(request.json['user_login']),
            header=str(request.json['header']),
            content=str(request.json['content']),
            status=str(request.json['status']),
            creation_date=str(request.json['creation_date'])
        )
        lecture_repository.update_lecture_fields(lecture)
        response = make_response("Lecture was successfully modified!")
        return response, 200
    elif request.method == 'DELETE':
        lecture_repository.delete_lecture_by_keys(
            str(request.json['user_login']),
            str(request.json['header'])
        )
        response = make_response("Lecture was successfully deleted!")
        return response, 200


@app.route('/api/lecture/<login>', methods=['GET'])
def api_lectures_of_owner(login):
    lecture_repository = LecturesRepository()
    lectures = lecture_repository.get_lectures_by_foreign_key(login)
    return serialize_array(lectures), 200


@app.route('/api/user/register', methods=['POST'])
def api_user_register():
    new_user = UserDTO(
        login=str(request.json['login']),
        role=str(request.json['role']),
        password=str(request.json['password']),
        registration_date=str(request.json['registration_date'])
    )

    status_message, status_code = user_service.register_user(new_user)
    return status_message


@app.route('/api/user/auth', methods=['POST'])
def api_user_auth():
    new_user = UserDTO(
        login=str(request.json['login']),
        role=None,
        password=str(request.json['password']),
        registration_date=None
    )

    status_message, status_code = user_service.auth_user(new_user)
    return status_message


@app.route('/api/user', methods=['PUT'])
def api_user_promotion():
    user_login = str(request.json['login'])
    new_user_role = str(request.json['new_role'])

    status_message, status_code = user_service.promote_user(user_login, new_user_role)
    return status_message
