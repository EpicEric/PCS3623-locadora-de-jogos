from board_game_store.db.access import add_room
from flask import Blueprint, flash, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

rooms_blueprint = Blueprint('rooms', __name__, template_folder='templates')


class AddRoomForm(FlaskForm):
    number = IntegerField('Número', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    seats = IntegerField('Lugares', validators=[DataRequired(), NumberRange(min=1, max=1000)])


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
