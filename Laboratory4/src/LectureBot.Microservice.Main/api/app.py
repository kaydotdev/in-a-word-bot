from flask import Flask, render_template, request, redirect, url_for, make_response

from dal.repository import Repository, UnitOfWork, ServiceLocator
from dal.models import Role, User, Lecture, UserHasResources, Resource, Component, Attribute
from dal.dbcontext import *

from api.forms import RoleForm, LectureForm, ResourceForm, RoleEditForm, LectureEditForm, ResourceEditForm, LoginForm
from api.settings.launch import SECRET

app = Flask(__name__)
app.secret_key = SECRET


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm.LoginForm(request.form)

    if request.method == 'POST':
        res = make_response("")
        res.set_cookie('user', form.Login.data, max_age=None)
        res.set_cookie('token', form.Password.data, max_age=None)
        res.headers['location'] = url_for('page')
        return res, 302

    if 'token' in request.cookies:
        return render_template('page.html', user=request.cookies['user'])
    else:
        return render_template('login.html', form=form)


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


@app.route('/user', methods=['GET'])
def list_users():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    users = repository.get_all(User.User)

    return render_template('user.html', users=users, user=request.cookies['user'])


@app.route('/lecture', methods=['GET', 'POST'])
def list_lectures():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    lectures = repository.get_all(Lecture.Lecture)
    form = LectureForm.LectureForm(request.form)

    if request.method == 'POST':
        new_lecture = Lecture.Lecture(header=form.Header.data, content=form.Content.data, userlogin=form.Owner.data)
        repository.create(new_lecture)
        unit_of_work.commit()
        return redirect('/lecture')

    return render_template('lecture.html', lectures=lectures, form=form, user=request.cookies['user'])


@app.route('/lecture/delete/<identity>', methods=['GET'])
def delete_lecture(identity):
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    repository.drop(Lecture.Lecture, identity, True)
    unit_of_work.commit()
    return redirect('/lecture')


@app.route('/lecture/edit/<identity>', methods=['GET'])
def edit_lecture(identity):
    form = LectureEditForm.LectureEditForm()
    form.id.data = identity
    return render_template('lectureedit.html', identity=identity, form=form, user=request.cookies['user'])


@app.route('/lectureedit', methods=['POST'])
def save_changes_lecture():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    form = LectureEditForm.LectureEditForm(request.form)

    new_lecture = Lecture.Lecture(header=form.Header.data, content=form.Content.data, userlogin=form.Owner.data)
    new_lecture.Id = form.id.data

    repository.update(Lecture.Lecture, new_lecture, form.id.data, True)
    unit_of_work.commit()
    return redirect('/lecture')
