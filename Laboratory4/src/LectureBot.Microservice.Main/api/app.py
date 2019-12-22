from flask import Flask, render_template, request, redirect, url_for, make_response

from dal.repository.LecturesRepository import LecturesRepository
from dal.repository.UserRepository import UserRepository
from dal.repository.RoleRepository import RoleRepository
from dal.repository.ResourceRepository import ResourceRepository
from dal.repository.UnitOfWork import UnitOfWork

from dal.dbcontext import *

from api.forms.LectureEditForm import LectureEditForm
from api.forms.LectureForm import LectureForm
from api.forms.LoginForm import LoginForm

from api.settings.launch import SECRET

from dal.models.Lecture import Lecture

app = Flask(__name__)
app.secret_key = SECRET


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

