from board_game_store.db.access import add_user
from flask import Blueprint, flash, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

clients_blueprint = Blueprint('clients', __name__, template_folder='templates')


class AddClientForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Sobrenome', validators=[DataRequired()])
    birthday = DateField('Aniversário', validators=[DataRequired()])


@clients_blueprint.route('/clients/add-client', methods=['GET', 'POST'])
def add_client_page():
    def error(message):
        flash(message)
        return redirect('/error')
    form = AddClientForm()
    if form.validate_on_submit():
        cpf = form.cpf.data
        if len(cpf) != 11 or any(x < '0' or x > '9' for x in cpf):
            return error('CPF deve possuir 11 dígitos numéricos')
        try:
            add_user(form.cpf.data, form.name.data, form.surname.data, form.birthday.data)
        except Exception as e:
            return error('Erro no banco de dados: {}'.format(e))
        return redirect('success')
    return render_template('clients/add_client.html', form=form)
