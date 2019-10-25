from flask import Flask, render_template, request, redirect, url_for

from LecturebotDAL.repository import Repository
from LecturebotDAL.models import Role, Resource

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

