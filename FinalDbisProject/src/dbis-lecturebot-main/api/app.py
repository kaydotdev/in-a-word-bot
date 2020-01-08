from flask import Flask, make_response, request, render_template, url_for, redirect

import datetime
import json

from api.settings.apisettings import API_SECRET

from api.forms.LoginForm import LoginForm
from api.forms.RegisterForm import RegisterForm

from bll.services.UserService import UserService
from bll.services.LecturesService import LecturesService
from bll.services.ResourcesService import ResourcesService

from bll.dto.UserDTO import UserDTO
from bll.dto.LectureDTO import LectureDTO


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
lecture_service = LecturesService()
resource_service = ResourcesService()


@app.route('/api/lecture', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_lecture():
    if request.method == 'GET':
        lectures = lecture_service.get_all_user_lectures('linus__torvalds')
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)

    if request.method == 'POST':
        message, status = user_service.auth_user(UserDTO(
            login=form.Login.data,
            password=form.Password.data,
            role=None,
            registration_date=None
        ))

        if status == 400:
            return render_template('login.html',
                                   form=form,
                                   message=message)

        res = make_response("")
        res.set_cookie('user', form.Login.data, max_age=None)
        res.set_cookie('token', form.Password.data, max_age=None)
        res.headers['location'] = url_for('page')
        return res, 302

    if 'token' in request.cookies:
        return render_template('page.html', user=request.cookies['user'])
    else:
        return render_template('login.html',
                               form=form,
                               message="")


@app.route('/page', methods=['GET'])
def page():
    if 'token' in request.cookies:
        return render_template('page.html', user=request.cookies['user'])
    else:
        return redirect('/logout')


@app.route('/logout', methods=['GET'])
def logout():
    res = make_response("")
    res.set_cookie('user', '', max_age=0)
    res.set_cookie('token', '', max_age=0)
    res.headers['location'] = url_for('index')
    return res, 302


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('register.html',
                                   form=form,
                                   message="Input data is not valid!")

        message, status = user_service.register_user(UserDTO(
            login=form.Login.data,
            password=form.Password.data,
            role="default_user",
            registration_date=datetime.date.today()
        ))

        if status == 400:
            return render_template('register.html',
                                   form=form,
                                   message=message)
        else:
            return redirect('/')

    return render_template('register.html',
                           form=form,
                           message="")
