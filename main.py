from data.jobs import Jobs
from data.users import User
from flask import *
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
        lst.append([job.id, job.job, user_fullname, str(duration.total_seconds() // 3600) + ' hours', job.collaborators, is_finished])
    return render_template('jobs_list.html', list=lst)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')