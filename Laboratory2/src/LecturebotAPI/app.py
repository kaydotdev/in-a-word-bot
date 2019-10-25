from flask import Flask, render_template, request, redirect, url_for

from LecturebotDAL.repository import Repository
from LecturebotDAL.models import Role, User, Lecture, UserHasResources, Resource

from LecturebotDAL.dbcontext import *

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET'])
def index():
    return render_template('navigation.html')


@app.route('/role', methods=['GET'])
def list_roles():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    roles = repository.get_all(Role.Role)

    return render_template('role.html', roles=roles)


@app.route('/user', methods=['GET'])
def list_users():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    users = repository.get_all(User.User)

    return render_template('user.html', users=users)


@app.route('/lecture', methods=['GET'])
def list_lectures():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    lectures = repository.get_all(Lecture.Lecture)

    return render_template('lecture.html', lectures=lectures)


@app.route('/userhasresources', methods=['GET'])
def list_resources_of_user():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    resources_of_user = repository.get_all(UserHasResources.UserHasResources)

    return render_template('userhasresource.html', usersresources=resources_of_user)


@app.route('/resource', methods=['GET'])
def list_resources():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    resources = repository.get_all(Resource.Resource)

    return render_template('resource.html', resources=resources)
