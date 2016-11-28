from board_game_store.db.access import add_client, get_all_client_names, get_client_info
from flask import Blueprint, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_login import login_required

clients_blueprint = Blueprint('clients', __name__, template_folder='templates')


class AddClientForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Sobrenome', validators=[DataRequired()])
    birthday = DateField('Aniversário', validators=[DataRequired()])


@clients_blueprint.route('/clients/add-client', methods=['GET', 'POST'])
@login_required
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
            add_client(form.cpf.data, form.name.data, form.surname.data, form.birthday.data)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    return render_template('clients/add_client.html', form=form)


@clients_blueprint.route('/clients/list-clients')
@login_required
def list_clients_page():
    def error(message):
        flash(message)
        return redirect('/error')
    try:
        client_list = get_all_client_names()
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    form = AddClientForm()
    return render_template('clients/list_clients.html', client_list=client_list, form=form)


@clients_blueprint.route('/clients/view-client')
@login_required
def view_client_page():
    def error(message):
        flash(message)
        return redirect('/error')
    try:
        client_cpf = request.args.get('cpf', '')
        client_tuple = get_client_info(client_cpf)
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    form = AddClientForm()

    form.cpf.data = client_tuple[0]
    form.name.data = client_tuple[1]
    form.surname.data = client_tuple[2]
    form.birthday.data = client_tuple[3]

    return render_template('clients/view_client.html', form=form)
