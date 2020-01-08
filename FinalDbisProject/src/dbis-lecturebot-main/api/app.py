from flask import Flask, make_response, request, render_template, url_for, redirect

import datetime
import json

from api.settings.apisettings import API_SECRET

from api.forms.LoginForm import LoginForm
from api.forms.RegisterForm import RegisterForm
from api.forms.LectureForm import LectureForm

from api.forms.LectureEditForm import LectureEditForm

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


@app.route('/lecture', methods=['GET', 'POST'])
def list_lectures():
    user_login = request.cookies['user']
    lectures = lecture_service.get_all_user_lectures(user_login)
    lectures_count = lecture_service.get_count_of_user_lectures(user_login)
    form = LectureForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('lecture.html',
                                   form=form,
                                   message="Input data is not valid!")

        new_lecture = LectureDTO(
            header=form.Header.data,
            content=form.Content.data,
            status="Pending",
            creation_date=datetime.date.today()
        )
        message, status = lecture_service.add_lecture(user_login, new_lecture)

        if status != 200:
            return render_template('lecture.html',
                                   lectures=lectures,
                                   form=form,
                                   user=user_login,
                                   lectures_count=lectures_count,
                                   message=message)
        else:
            return redirect('/lecture')

    return render_template('lecture.html',
                           lectures=lectures,
                           form=form,
                           user=user_login,
                           lectures_count=lectures_count,
                           message="")


@app.route('/profile', methods=['GET'])
def profile():
    user_login = request.cookies['user']
    count_of_resources = resource_service.get_count_of_user_resources(user_login)
    count_of_lectures = lecture_service.get_count_of_user_lectures(user_login)
    user = user_service.get_user_by_login(user_login)

    user.Role = ' '.join(user.Role.split('_')).upper()

    return render_template('profile.html',
                           user=user_login,
                           count_of_resources=count_of_resources,
                           count_of_lectures=count_of_lectures,
                           user_role=user.Role)


@app.route('/lecture/edit', methods=['GET', 'POST'])
def edit_lecture_page():
    user_login = request.cookies['user']
    lecture_to_edit = request.cookies['lecture_header']

    form = LectureEditForm()

    form.Content.data = lecture_service.get_lecture_by_login_and_header(user_login, lecture_to_edit)[0].Content
    return render_template('lecture_update.html',
                           form=form,
                           header=lecture_to_edit,
                           user=user_login)


@app.route('/api/lecture', methods=['POST'])
def api_lecture():
    user_login = request.cookies['user']
    lecture_header = request.cookies['lecture_header']
    lecture_to_edit = lecture_service.get_lecture_by_login_and_header(user_login, lecture_header)[0]

    form = LectureEditForm(request.form)

    lecture = LectureDTO(
        header=lecture_to_edit.Header,
        content=form.Content.data,
        status=lecture_to_edit.Status,
        creation_date=lecture_to_edit.Creation_Date
    )

    message, status = lecture_service.edit_lecture(user_login, lecture_to_edit.Header, lecture)
    if status == 200:
        res = make_response("")
        res.set_cookie('lecture_header', '', max_age=0)
        res.headers['location'] = url_for('list_lectures')
        return res, 302
    else:
        return redirect('/lecture/edit')


@app.route('/lecture/delete', methods=['GET', 'POST'])
def delete_lecture():
    user_login = request.cookies['user']
    lecture_to_delete = request.cookies['lecture_header']
    lecture_service.delete_lecture(user_login, lecture_to_delete)
    res = make_response("")
    res.set_cookie('lecture_header', '', max_age=0)
    res.headers['location'] = url_for('list_lectures')
    return res, 302
