from flask import Flask, render_template, request, redirect, url_for, make_response

from dal.repository.LecturesRepository import LecturesRepository
from dal.repository.UserRepository import UserRepository
from dal.repository.RoleRepository import RoleRepository
from dal.repository.ResourceRepository import ResourceRepository
from dal.repository.UnitOfWork import UnitOfWork

from dal.dbcontext import *

from api.forms.LectureEditForm import LectureEditForm
from api.forms.ResourceEditForm import ResourceEditForm

from api.forms.GenerateLectureForm import GenerateLectureForm
from api.forms.LectureForm import LectureForm
from api.forms.ResourceForm import ResourceForm

from api.forms.LoginForm import LoginForm
from api.forms.RegisterForm import RegisterForm

from api.settings.launch import SECRET
from api.settings.urls import AI_SERVICE_URL

from dal.models.Lecture import Lecture
from dal.models.Resource import Resource
from dal.models.User import User

from datetime import date

import hmac
import hashlib
import requests


app = Flask(__name__)
app.secret_key = SECRET


def get_password_hash(salt, password):
    return hmac.new(bytes(salt, 'UTF-8'), msg=bytes(password, 'UTF-8'), digestmod=hashlib.sha256).hexdigest().upper()


def ping_ai_service(theme):
    req = requests.post(AI_SERVICE_URL, json={'theme': theme})

    if req.status_code == 500:
        return "Sorry, generating service is not available now!"
    elif req.status_code == 400:
        return "Wrong input data!"
    else:
        response = req.content
        return response


@app.route('/', methods=['GET', 'POST'])
def index():
    user_repository = UserRepository(session, ModelBase, DBEngine)
    form = LoginForm(request.form)

    if request.method == 'POST':
        user = user_repository.get_user_by_login(form.Login.data)

        if len(user) == 0:
            return render_template('login.html', form=form, failed_login=True)

        res = make_response("")
        res.set_cookie('user', form.Login.data, max_age=None)
        res.set_cookie('token', form.Password.data, max_age=None)
        res.headers['location'] = url_for('page')
        return res, 302

    if 'token' in request.cookies:
        return render_template('page.html', user=request.cookies['user'])
    else:
        return render_template('login.html', form=form, failed_login=False)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    user_repository = UserRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)
    form = RegisterForm(request.form)

    if request.method == 'POST':
        new_user = User(login=form.Login.data, password=str(get_password_hash(SECRET, form.Password.data)), regdate=str(date.today()), roleid=2)
        user_repository.create(new_user)
        unit_of_work.commit()
        return redirect('/')

    return render_template('register.html', form=form, failed_login=False)


@app.route('/logout', methods=['GET'])
def logout():
    res = make_response("")
    res.set_cookie('user', '', max_age=0)
    res.set_cookie('token', '', max_age=0)
    res.headers['location'] = url_for('index')
    return res, 302


@app.route('/page', methods=['GET'])
def page():
    return render_template('page.html', user=request.cookies['user'])


@app.route('/lecture', methods=['GET', 'POST'])
def list_lectures():
    user_login = request.cookies['user']
    lectures_repository = LecturesRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)
    lectures = lectures_repository.get_lectures_of_user(user_login)
    lectures_count = lectures_repository.get_amount_of_lectures_of_user(user_login)

    l_count = [str(lecture_count.Lectures) for lecture_count in lectures_count]

    form = LectureForm(request.form)

    if request.method == 'POST':
        new_lecture = Lecture(header=form.Header.data, content=form.Content.data, userlogin=user_login)
        lectures_repository.create(new_lecture)
        unit_of_work.commit()
        return redirect('/lecture')

    return render_template('lecture.html', lectures=lectures, form=form, user=user_login, lectures_count=l_count[0])


@app.route('/lecture/delete/<identity>', methods=['GET'])
def delete_lecture(identity):
    repository = LecturesRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)
    repository.drop_lecture(identity)
    unit_of_work.commit()
    return redirect('/lecture')


@app.route('/lecture/edit/<identity>', methods=['GET'])
def edit_lecture(identity):
    user_login = request.cookies['user']
    form = LectureEditForm()
    form.id.data = identity

    lectures_repository = LecturesRepository(session, ModelBase, DBEngine)

    form.Header.data = lectures_repository.get_lecture_by_id(identity).Header
    form.Content.data = lectures_repository.get_lecture_by_id(identity).Content

    return render_template('lecture_update.html', identity=identity, form=form, user=user_login)


@app.route('/update_lecture', methods=['POST'])
def update_lecture():
    user_login = request.cookies['user']
    repository = LecturesRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)
    form = LectureEditForm(request.form)

    new_lecture = Lecture(header=form.Header.data, content=form.Content.data, userlogin=user_login)
    new_lecture.Id = form.id.data

    repository.update_lecture(form.id.data, new_lecture)
    unit_of_work.commit()
    return redirect('/lecture')


@app.route('/profile', methods=['GET'])
def profile():
    user_login = request.cookies['user']
    lectures_repository = LecturesRepository(session, ModelBase, DBEngine)
    lectures_count = lectures_repository.get_amount_of_lectures_of_user(user_login)
    l_count = [str(lecture_count.Lectures) for lecture_count in lectures_count][0]

    roles_repository = RoleRepository(session, ModelBase, DBEngine)
    role_of_user = roles_repository.get_user_role(user_login)
    r_user = [str(r.Name) for r in role_of_user][0]

    resource_repository = ResourceRepository(session, ModelBase, DBEngine)
    resources_of_user = resource_repository.get_amount_of_resources_of_user(user_login)
    res_user = [str(r.URLS) for r in resources_of_user][0]

    return render_template('profile.html',
                           user=request.cookies['user'],
                           lectures_count=l_count,
                           user_role=r_user,
                           user_resources=res_user)


@app.route('/resources', methods=['GET', 'POST'])
def list_resources():
    user_login = request.cookies['user']
    resource_repository = ResourceRepository(session, ModelBase, DBEngine)
    query_resources = resource_repository.get_resources_of_user(user_login)

    user_resources = [Resource(res.URL, res.Description, res.TimesVisited) for res in query_resources]

    resource_repository = ResourceRepository(session, ModelBase, DBEngine)
    resources_of_user = resource_repository.get_amount_of_resources_of_user(user_login)
    r_count = [str(r.URLS) for r in resources_of_user][0]

    unit_of_work = UnitOfWork(session, ModelBase)

    form = ResourceForm(request.form)

    if request.method == 'POST':
        new_resource = Resource(url=form.URL.data, description=form.Description.data, times_visited=1)
        resource_repository.create(new_resource)
        unit_of_work.commit()
        resource_repository.insert_user_and_resource_relation(user_login, new_resource.URL)
        unit_of_work.commit()
        return redirect('/resources')

    return render_template('resource.html',
                           user=user_login,
                           user_resources=user_resources,
                           resources_count=r_count,
                           form=form)


@app.route('/resource/edit', methods=['GET'])
def edit_resources():
    url_query = request.cookies['resource_url']
    user_login = request.cookies['user']
    form = ResourceEditForm()

    resource_repository = ResourceRepository(session, ModelBase, DBEngine)
    resource_to_edit = resource_repository.get_by_url(url_query)

    form.Url.data = resource_to_edit.URL
    form.Description.data = resource_to_edit.Description

    return render_template('resource_update.html',
                           form=form,
                           user=user_login)


@app.route('/update_resource', methods=['GET', 'POST'])
def update_resource():
    form = ResourceEditForm(request.form)
    resource_repository = ResourceRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)
    new_resource = Resource(url=form.Url.data, description=form.Description.data, times_visited=1)

    resource_repository.update_resource(new_resource.URL, new_resource)
    unit_of_work.commit()

    res = make_response("")
    res.set_cookie('resource_url', '', max_age=0)
    res.headers['location'] = url_for('list_resources')
    return res, 302


@app.route('/resource/delete', methods=['GET'])
def delete_resource():
    user_login = request.cookies['user']
    url_query = request.cookies['resource_url']

    repository = ResourceRepository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork(session, ModelBase)

    repository.drop_user_and_resource_relation(user_login, url_query)
    unit_of_work.commit()

    repository.drop_resource(url_query)
    unit_of_work.commit()

    res = make_response("")
    res.set_cookie('resource_url', '', max_age=0)
    res.headers['location'] = url_for('list_resources')
    return res, 302


@app.route('/new_lecture', methods=['GET', 'POST'])
def lecture_generator():
    form = GenerateLectureForm()
    user_login = request.cookies['user']
    return render_template('new_lecture.html',
                           form=form,
                           user=user_login)


@app.route('/make_lecture', methods=['POST'])
def make_lecture():
    form = GenerateLectureForm(request.form)
    if form.Header.data:
        return ping_ai_service(form.Header.data)
    else:
        return ""
