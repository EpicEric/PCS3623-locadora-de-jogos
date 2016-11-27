from board_game_store.db.access import add_room, get_all_room_numbers, get_free_rooms
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange

rooms_blueprint = Blueprint('rooms', __name__, template_folder='templates')


class AddRoomForm(FlaskForm):
    number = IntegerField('Número', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    seats = IntegerField('Lugares', validators=[DataRequired(), NumberRange(min=1, max=1000)])


class ViewRoomForm(FlaskForm):
    seats = IntegerField('Número de pessoas', validators=[DataRequired(), NumberRange(min=1, max=30)])
    date = DateField('Dia')
    time = StringField('Horário')


@rooms_blueprint.route('/rooms/add-room', methods=['GET', 'POST'])
def add_rooms_page():
    def error(message):
        flash(message)
        return redirect('/error')
    form = AddRoomForm()
    if form.validate_on_submit():
        try:
            add_room(form.number.data, form.seats.data)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    return render_template('rooms/add_room.html', form=form)


@rooms_blueprint.route('/rooms/view-room', methods=['GET', 'POST'])
def view_rooms_page():
    def error(message):
        flash(message)
        return redirect('/error')
    form = ViewRoomForm()
    if form.validate_on_submit():
        try:
            desired_time = '{} {}'.format(form.date.data, form.time.data)
            return render_template(
                'rooms/view_room.html',
                rooms=get_free_rooms(form.seats.data, datetime.strptime(desired_time, '%Y-%m-%d %H:%M')))
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    return render_template('rooms/view_room_form.html', form=form)
