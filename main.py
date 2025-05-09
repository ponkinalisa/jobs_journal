from data.jobs import Jobs
from data.users import User
from data.login import LoginForm
from data.registration import Registration
from data.new_job import NewJob, EditJob, DeleteJob
from flask import *
from data import db_session, jobs_api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': '505'}), 500)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    if current_user.__class__.__name__ == 'User':
        return render_template('login.html', title='Авторизация', form=form, username=current_user.name)
    return render_template('login.html', title='Авторизация', form=form, username='пользователь')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user:
                return render_template('registration.html',
                                       message="пользователь с такой почтой уже зарегистрирован", form=form)
            user = db_sess.query(User).filter(User.address == form.address.data).first()
            if user:
                return render_template('registration.html',
                                       message="пользователь с таким адресом уже зарегистрирован", form=form)
            user = User()
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            user.email = form.email.data
            user.set_password(form.hashed_password.data)
            if form.modified_date.data:
                user.modified_date = form.modified_date.data
            else:
                user.modified_date = datetime.datetime.now
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        except Exception as e:
            return render_template('registration.html',
                                   message=e, form=form)
    if current_user.__class__.__name__ == 'User':
        return render_template('registration.html', title='Регистрация', form=form, username=current_user.name)
    return render_template('registration.html', title='Регистрация', form=form, username='пользователь')


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/edit_job/<id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = EditJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if current_user.id != jobs.team_leader and current_user.id != 1:
            return render_template('edit_job.html', title='Редактирование работы', form=form,
                                   username=current_user.name, message="Вы не можете редактировать данную работу")
        jobs.team_leader = form.team_leader.data
        if form.job.data:
            jobs.job = form.job.data
        if form.work_size.data:
            jobs.work_size = form.work_size.data
        if form.collaborators.data:
            jobs.collaborators = form.collaborators.data
        if form.start_date.data:
            jobs.start_date = form.start_date.data
        if form.end_date.data:
            jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    if current_user.__class__.__name__ == 'User':
        return render_template('edit_job.html', title='Редактирование работы', form=form, username=current_user.name)
    return render_template('edit_job.html', title='Редактирование работы', form=form, username='пользователь')


@app.route('/new_job', methods=['GET', 'POST'])
@login_required
def new_job():
    form = NewJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    if current_user.__class__.__name__ == 'User':
        return render_template('new_job.html', title='Добавление работы', form=form, username=current_user.name)
    return render_template('new_job.html', title='Добавление работы', form=form, username='пользователь')


@app.route('/delete_job/<id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if current_user.id != jobs.team_leader and current_user.id != 1:
        redirect('/')  # пользователь не обладает правами на удаление
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')



@app.route('/')
def main():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    lst = []
    for job in jobs:
        try:
            user = db_sess.query(User).filter(User.id == job.team_leader).first()
            user_fullname = user.name + ' ' + user.surname
            is_finished = 'Is not finished'
            duration = job.end_date - job.start_date
            if job.is_finished:
                is_finished = 'Is finished'
            lst.append(
                [job.id, job.job, user_fullname, str(duration.total_seconds() // 3600) + ' hours', job.collaborators,
                 is_finished])
        except Exception:
            break
    if current_user.__class__.__name__ == 'User':
        return render_template('jobs_list.html', list=lst, username=current_user.name)
    return render_template('jobs_list.html', title='Главная',  username='пользователь', list=lst)



if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=80, host='127.0.0.1')
