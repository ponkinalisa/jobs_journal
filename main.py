from data.jobs import Jobs
from data.users import User
from data.login import LoginForm
from data.new_job import NewJob
from flask import *
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
        if user and user.hashed_password == form.password.data:  # так как при добавлении в бд хэширования еще не было
            login_user(user, remember=form.remember_me.data)  # то для корректного тестирования его и тут нет
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    if current_user.__class__.__name__ == 'User':
        return render_template('login.html', title='Авторизация', form=form, username=current_user.name)
    return render_template('login.html', title='Авторизация', form=form, username='пользователь')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/new_job', methods=['GET', 'POST'])
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
    return render_template('new_job.html', title='Добавление работы', form=form, username='пользователь')


@app.route('/')
def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    lst = []
    for job in jobs:
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        user_fullname = user.name + ' ' + user.surname
        is_finished = 'Is not finished'
        duration = job.end_date - job.start_date
        if job.is_finished:
            is_finished = 'Is finished'
        lst.append([job.id, job.job, user_fullname, str(duration.total_seconds() // 3600) + ' hours', job.collaborators,
                    is_finished])
    if current_user.__class__.__name__ == 'User':
        return render_template('jobs_list.html', list=lst, username=current_user.name)
    return render_template('jobs_list.html', title='Главная',  username='пользователь', list=lst)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
