from flask import Flask, render_template, request, redirect, url_for

from LecturebotDAL.repository import Repository
from LecturebotDAL.models import Role, User

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

