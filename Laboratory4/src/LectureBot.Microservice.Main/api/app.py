from flask import Flask, render_template, request, redirect, url_for, make_response

from dal.repository.LecturesRepository import LecturesRepository
from dal.repository.UserRepository import UserRepository
from dal.repository.UnitOfWork import UnitOfWork

from dal.dbcontext import *

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

