from board_game_store.db.access import add_reservation, add_room, get_all_rooms, get_free_rooms, get_room_info, get_all_reserves, get_reservation_info, get_room_reservations
from datetime import datetime
from flask import Blueprint, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange
from flask_login import current_user, login_required

rooms_blueprint = Blueprint('rooms', __name__, template_folder='templates')


class AddRoomForm(FlaskForm):
    number = IntegerField('Número', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    seats = IntegerField('Lugares', validators=[DataRequired(), NumberRange(min=1, max=1000)])


class ViewRoomForm(FlaskForm):
    seats = IntegerField('Número de pessoas', validators=[DataRequired(), NumberRange(min=1, max=30)])
    date = DateField('Dia', validators=[DataRequired()])
    time = StringField('Horário de início', validators=[DataRequired()])
    room = SelectField('Salas disponíveis')
    end_time = StringField('Horário de fim')
    client_cpf = StringField('CPF do cliente')


class ViewReservationForm(FlaskForm):
    room_number = IntegerField('Número da sala', validators=[DataRequired()])
    start_time = StringField('Horário de início', validators=[DataRequired()])
    end_time = StringField('Horário de término', validators=[DataRequired()])
    client_cpf = StringField('CPF do cliente', validators=[DataRequired()])
    employee_cpf = StringField('CPF do funcionário', validators=[DataRequired()])


@rooms_blueprint.route('/rooms')
@login_required
def default_rooms_page():
    return redirect("/rooms/list-rooms")


@rooms_blueprint.route('/rooms/add-room', methods=['GET', 'POST'])
@login_required
def add_rooms_page():
    form = AddRoomForm()
    if form.validate_on_submit():
        add_room(form.number.data, form.seats.data)
        return redirect('success')
    return render_template('rooms/add_room.html', form=form)


@rooms_blueprint.route('/rooms/list-rooms')
@login_required
def list_rooms_page():
    room_list = get_all_rooms()
    return render_template('rooms/list_rooms.html', room_list=room_list)


@rooms_blueprint.route('/rooms/view-room')
@login_required
def view_room_page():
    room_number = request.args.get('number', '')
    room_tuple = get_room_info(room_number)

    form = AddRoomForm()

    form.number.data = room_tuple[0]
    form.seats.data = room_tuple[1]

    reservations = get_room_reservations(room_number)

    return render_template('rooms/view_room.html', form=form, reservations=reservations)


@rooms_blueprint.route('/rooms/reserve-room', methods=['GET', 'POST'])
@login_required
def reserve_room_page():
    form = ViewRoomForm()
    if request.method == 'POST':
        desired_time = datetime.strptime('{} {}'.format(form.date.data, form.time.data), '%Y-%m-%d %H:%M')
        if form.room.data != 'None':
            end_time = datetime.strptime('{} {}'.format(form.date.data, form.end_time.data), '%Y-%m-%d %H:%M')
            if end_time < desired_time:
                raise RuntimeError('Tempo de fim deve ser maior que tempo de início')
            add_reservation(form.room.data, desired_time, end_time, form.client_cpf.data, current_user.get_id())
            return redirect('success')
        else:
            form.room.choices = [
                (x[0], '{} - {}'.format(x[0], x[1] and 'Livre até {}'.format(x[1]) or 'Sem reserva futura'))
                for x in get_free_rooms(form.seats.data, desired_time)
            ]
            return render_template('rooms/reserve_room.html', form=form)
    return render_template('rooms/reserve_room.html', form=form)


@rooms_blueprint.route('/rooms/list-reserves')
@login_required
def list_reserves_page():
    reserve_list = get_all_reserves()
    return render_template('rooms/list_reserves.html', reserve_list=reserve_list)


@rooms_blueprint.route('/rooms/view-reserve')
@login_required
def view_reserve_page():
    room_number = request.args.get('number', '')
    start_time = request.args.get('time', '')
    reservation_tuple = get_reservation_info(room_number, start_time)

    form = ViewReservationForm()

    form.room_number.data = reservation_tuple[0]
    form.start_time.data = reservation_tuple[1]
    form.end_time.data = reservation_tuple[2]
    form.client_cpf.data = reservation_tuple[3]
    form.employee_cpf.data = reservation_tuple[4]

    return render_template('rooms/view_reserve.html', form=form)
