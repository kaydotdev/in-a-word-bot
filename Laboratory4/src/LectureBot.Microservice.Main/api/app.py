from flask import Flask, render_template, request, redirect

from dal.repository import Repository, UnitOfWork, ServiceLocator
from dal.models import Role, User, Lecture, UserHasResources, Resource, Component, Attribute
from dal.dbcontext import *

from api.forms import RoleForm, LectureForm, ResourceForm, RoleEditForm, LectureEditForm, ResourceEditForm

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET'])
def index():
    return render_template('navigation.html')


@app.route('/role', methods=['GET', 'POST'])
def list_roles():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    roles = repository.get_all(Role.Role)
    form = RoleForm.RoleForm(request.form)

    if request.method == 'POST':
        new_role = Role.Role(name=form.Name.data, priority=form.Priority.data)
        repository.create(new_role)
        unit_of_work.commit()
        return redirect('/role')

    return render_template('role.html', roles=roles, form=form)


@app.route('/role/delete/<identity>', methods=['GET'])
def delete_role(identity):
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    repository.drop(Role.Role, identity, True)
    unit_of_work.commit()
    return redirect('/role')


@app.route('/role/edit/<identity>', methods=['GET'])
def edit_role(identity):
    form = RoleEditForm.RoleEditForm()
    form.id.data = identity
    return render_template('roleedit.html', identity=identity, form=form)


@app.route('/roleedit', methods=['POST'])
def save_changes_role():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    form = RoleEditForm.RoleEditForm(request.form)

    new_role = Role.Role(name=form.Name.data, priority=form.Priority.data)
    new_role.Id = form.id.data

    repository.update(Role.Role, new_role, form.id.data, True)
    unit_of_work.commit()
    return redirect('/role')


@app.route('/user', methods=['GET'])
def list_users():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    users = repository.get_all(User.User)

    return render_template('user.html', users=users)


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

    return render_template('lecture.html', lectures=lectures, form=form)


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
    return render_template('lectureedit.html', identity=identity, form=form)


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


@app.route('/userhasresources', methods=['GET'])
def list_resources_of_user():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    resources_of_user = repository.get_all(UserHasResources.UserHasResources)

    return render_template('userhasresource.html', usersresources=resources_of_user)


@app.route('/resource', methods=['GET', 'POST'])
def list_resources():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    resources = repository.get_all(Resource.Resource)
    form = ResourceForm.ResourceForm(request.form)

    if request.method == 'POST':
        new_resource = Resource.Resource(url=form.URL.data, description=form.Description.data)
        repository.create(new_resource)
        unit_of_work.commit()
        return redirect('/resource')

    return render_template('resource.html', resources=resources, form=form)


@app.route('/resource/delete/(<url>)', methods=['GET'])
def delete_resource(url):
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    repository.drop(Resource.Resource, url, False)
    unit_of_work.commit()
    return redirect('/lecture')


@app.route('/resource/edit/(<url>)', methods=['GET'])
def edit_resource(url):
    form = LectureEditForm.LectureEditForm()
    form.id.data = url
    return render_template('lectureedit.html', identity=url, form=form)


@app.route('/resourceedit', methods=['POST'])
def save_changes_resource():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    unit_of_work = UnitOfWork.UnitOfWork(session, ModelBase)
    form = ResourceEditForm.ResourceEditForm(request.form)

    new_resource = Resource.Resource(url=form.id.data, description=form.Description.data)

    repository.update(Resource.Resource, new_resource, form.id.data, False)
    unit_of_work.commit()
    return redirect('/resource')


@app.route('/component', methods=['GET'])
def list_components():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    components = repository.get_all(Component.Component)

    return render_template('component.html', components=components)


@app.route('/attribute', methods=['GET'])
def list_attributes():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    attributes = repository.get_all(Attribute.Attribute)

    return render_template('attribute.html', attributes=attributes)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    repository = Repository.Repository(session, ModelBase, DBEngine)
    resources = repository.get_all(Resource.Resource)

    repository = ServiceLocator.ServiceLocator(session, ModelBase, DBEngine)
    res_count = repository.get_count_of_resources_of_user().fetchall()

    urls = [str(resource.URL) for resource in resources]
    times = [int(resource.TimesVisited) for resource in resources]

    res = [str(resC[0]) for resC in res_count]
    count = [int(resC[1]) for resC in res_count]

    return render_template('dashboard.html', x1=urls, y1=times, x2=res, y2=count)
