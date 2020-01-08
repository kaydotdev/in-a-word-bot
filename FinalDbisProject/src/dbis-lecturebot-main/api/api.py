from flask import make_response, request

from api.app import app, serialize_array, user_service, lecture_service, resource_service

from bll.dto.UserDTO import UserDTO
from bll.dto.LectureDTO import LectureDTO


@app.route('/api/lecture', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_lecture():
    if request.method == 'GET':
        lectures = lecture_service.get_all_user_lectures(str(request.json['login']))
        return serialize_array(lectures), 200
    elif request.method == 'POST':
        lecture = LectureDTO(
            header=str(request.json['header']),
            content=str(request.json['content']),
            status=str(request.json['status']),
            creation_date=str(request.json['creation_date'])
        )
        message, status = lecture_service.add_lecture(str(request.json['user_login']), lecture)
        response = make_response(message)
        return response, status
    elif request.method == 'PUT':
        lecture = LectureDTO(
            header=str(request.json['header']),
            content=str(request.json['content']),
            status=str(request.json['status']),
            creation_date=str(request.json['creation_date'])
        )
        message, status = lecture_service.edit_lecture(
            str(request.json['user_login']),
            str(request.json['header']),
            lecture)
        response = make_response(message)
        return response, status
    elif request.method == 'DELETE':
        user = UserDTO(
            login=str(request.json['user_login']),
            role=None,
            password=None,
            registration_date=None
        )

        lecture = LectureDTO(
            header=str(request.json['header']),
            content=None,
            status=None,
            creation_date=None
        )

        lecture_service.delete_lecture(user, lecture)
        response = make_response("Lecture was successfully deleted!")
        return response, 200


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


@app.route('/api/user/role/<login>', methods=['GET'])
def api_get_role_by_login(login):
    user = user_service.get_user_by_login(login)

    if user:
        return user.Role
    else:
        return "", 204
