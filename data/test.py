from requests import get, post, delete


def test_all_jobs():  # получение всех работ
    if get('http://127.0.0.1:80/api/jobs').json():
        return 'ok'
    return 'error'


def test_one_job_exist_correct():
    if get('http://127.0.0.1:80/api/jobs/3').json():
        return 'ok'
    return 'error'


def test_one_job_exist_incorrect():
    if 'error' in get('http://127.0.0.1:80/api/jobs/10129291920').json():
        return 'ok'
    return 'error'


def test_one_job_exist_string():
    if 'error' in  get('http://127.0.0.1:80/api/jobs/шла саша по шоссе и сосала сушку').json():
        return 'ok'
    return 'error'


def test_create_corr():  # правильный запрос
    if 'id' in post('http://127.0.0.1:80/api/jobs', json={'team_leader': 2, 'job': 'Текст новости', 'work_size': 1,
                                                    'collaborators': '1, 2, 3',
                                                    'start_date': '2025-04-13 00:00:00.000000',
                                                    'end_date': '2025-04-13 00:01:00.000000',
                                                    'is_finished': False}).json():
        return 'ok'
    return 'error'


def test_create_bool():  # все поля пустые
    if 'error' in post('http://127.0.0.1:80/api/jobs', json={}).json():
        return 'ok'
    return 'error'


def test_create_some_fields_bool():  # не все поля заполнены
    if 'error' in post('http://127.0.0.1:80/api/jobs', json={'team_leader': 'djkzdsnksda', 'job': 'Текст новости',
                                                    'start_date': '2025-04-13 00:00:00.000000',
                                                    'end_date': '2025-04-13 00:01:00.000000',
                                                    'is_finished': False}).json():
        return 'ok'
    return 'error'


def test_create_wrong_type():  # еправильный формат (не число) id лидера
    if 'error' in post('http://127.0.0.1:80/api/jobs', json={'team_leader': 'djkzdsnksda', 'job': 'Текст новости', 'work_size': 1,
                                                    'collaborators': '1, 2, 3',
                                                    'start_date': '2025-04-13 00:00:00.000000',
                                                    'end_date': '2025-04-13 00:01:00.000000',
                                                    'is_finished': False}).json():
        return 'ok'
    return 'error'


def test_delete_corr():
    if 'id' in delete('http://127.0.0.1:80/api/jobs/4').json():
        return 'ok'
    return 'error'


def test_delete_bool():
    if 'error' in delete('http://127.0.0.1:80/api/jobs/').json():
        return 'ok'
    return 'error'


def test_delete_incorr():
    if 'error' in delete('http://127.0.0.1:80/api/jobs/23627636273').json():
        return 'ok'
    return 'error'


def test_edit_corr():  # правильный запрос
    if 'id' in post('http://127.0.0.1:80/api/jobs/edit/5', json={'team_leader': 3, 'job': 'dhsdsh', 'work_size': 1,
                                                    'collaborators': '1, 2, 3',
                                                    'start_date': '2024-04-13 00:00:00.000000',
                                                    'end_date': '2024-04-13 00:01:00.000000',
                                                    'is_finished': False}).json():
        return 'ok'
    return 'error'


def test_edit_bool():  # все поля пустые
    if 'error' in post('http://127.0.0.1:80/api/jobs/edit/5', json={}).json():
        return 'ok'
    return 'error'


def test_edit_incorr_id():
    if 'error' in post('http://127.0.0.1:80/api/jobs/edit/574746464',  json={'team_leader': 2, 'job': 'Текст новости', 'work_size': 1,
                                                    'collaborators': '1, 2, 3',
                                                    'start_date': '2025-04-13 00:00:00.000000',
                                                    'end_date': '2025-04-13 00:01:00.000000',
                                                    'is_finished': False}).json():
        return 'ok'
    return 'error'


def test_edit_wrong_type():  # неправильный формат (не число) id лидера
    if 'error' in post('http://127.0.0.1:80/api/jobs/edit/6', json={'team_leader': 'djkzdsnksda',
                                                                    'job': 'Текст новости', 'work_size': 1,
                                                                    'collaborators': '1, 2, 3', 'start_date':
                                                                    '2025-04-13 00:00:00.000000', 'end_date':
                                                                    '2025-04-13 00:01:00.000000', 'is_finished':
                                                                    False}).json():
        return 'ok'
    return 'error'


print(test_edit_corr(), test_edit_bool(), test_edit_incorr_id(), test_edit_wrong_type(), test_all_jobs())