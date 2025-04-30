from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField, BooleanField, StringField
from wtforms.validators import DataRequired


class NewJob(FlaskForm):
    team_leader = IntegerField('ID лидера команды', validators=[DataRequired()])
    job = StringField('Описание работы')
    work_size = IntegerField('Объем работы в часах')
    collaborators = StringField('Список id участников')
    start_date = DateField('дата начала')
    end_date = DateField('дата окончания')
    is_finished = BooleanField('Задача завершена')
    submit = SubmitField('Добавить работу')


class EditJob(FlaskForm):
    id = IntegerField('ID работы', validators=[DataRequired()])
    team_leader = IntegerField('ID лидера команды', validators=[DataRequired()])
    job = StringField('Описание работы')
    work_size = IntegerField('Объем работы в часах')
    collaborators = StringField('Список id участников')
    start_date = DateField('дата начала')
    end_date = DateField('дата окончания')
    is_finished = BooleanField('Задача завершена')
    submit = SubmitField('Редактировать работу')


class DeleteJob(FlaskForm):
    id = IntegerField('ID работы', validators=[DataRequired()])
    submit = SubmitField('Удалить работу')