from flask import *

from . import db_session

from .jobs import Jobs

from datetime import datetime


blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)



@blueprint.route('/api/jobs')
def api_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'work_size', 'collaborators', 'job', 'start_date',
                                    'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def api_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not isinstance(job_id, int):
        return 'Неверный формат запроса'
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'job':
                jobs.to_dict(only=('id', 'team_leader', 'work_size', 'collaborators', 'job', 'start_date',
                                    'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        if not (isinstance(request.json['team_leader'], int) and isinstance(request.json['work_size'], int) and
                isinstance(request.json['is_finished'], bool)):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        jobs = Jobs(
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            start_date=datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S.%f'),
            end_date=datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S.%f'),
            is_finished=request.json['is_finished'],
        )
        db_sess.add(jobs)
        db_sess.commit()
        return make_response(jsonify({'id': jobs.id}), 200)
    except Exception as e:
        return make_response(jsonify({'error': e}), 400)



@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not isinstance(job_id, int):
        return make_response(jsonify({'error': 'Неверный формат запроса'}), 500)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return make_response(jsonify({'id': f'Была удалена запись с id {job_id}'}), 200)


@blueprint.route('/api/jobs/edit/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        if not (isinstance(job_id, int) and isinstance(request.json['team_leader'], int) and isinstance(request.json['work_size'], int) and
                isinstance(request.json['is_finished'], bool)):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if not jobs:
            return make_response(jsonify({'error': 'Not found'}), 404)
        jobs.team_leader = request.json['team_leader']
        jobs.job = request.json['job']
        jobs.work_size = request.json['work_size']
        jobs.collaborators = request.json['collaborators']
        jobs.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S.%f')
        jobs.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S.%f')
        jobs.is_finished = request.json['is_finished']
        db_sess.add(jobs)
        db_sess.commit()
        return make_response(jsonify({'id': jobs.id}), 200)
    except Exception as e:
        return make_response(jsonify({'error': e}), 400)