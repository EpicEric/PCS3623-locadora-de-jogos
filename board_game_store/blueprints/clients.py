from board_game_store.db.access import add_client, get_all_client_names, get_client_info, get_rentals_by_client, get_purchases_by_client, get_reservations_by_client
from flask import Blueprint, redirect, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_login import login_required
from .errors import flash_errors

clients_blueprint = Blueprint('clients', __name__, template_folder='templates')


class AddClientForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Sobrenome', validators=[DataRequired()])
    birthday = DateField('Aniversário', validators=[DataRequired()])


@clients_blueprint.route('/clients')
@login_required
def default_clients_page():
    return redirect("/clients/list-clients")


@clients_blueprint.route('/clients/add-client', methods=['GET', 'POST'])
@login_required
def add_client_page():
    form = AddClientForm()
    if form.validate_on_submit():
        cpf = form.cpf.data
        if len(cpf) != 11 or any(x < '0' or x > '9' for x in cpf):
            raise RuntimeError('CPF deve possuir 11 dígitos numéricos')
        add_client(form.cpf.data, form.name.data, form.surname.data, form.birthday.data)
        return redirect('success')
    else:
        flash_errors(form)
    return render_template('clients/add_client.html', form=form)


@clients_blueprint.route('/clients/list-clients')
@login_required
def list_clients_page():
    client_list = get_all_client_names()
    form = AddClientForm()
    return render_template('clients/list_clients.html', client_list=client_list, form=form)


@clients_blueprint.route('/clients/view-client')
@login_required
def view_client_page():
    client_cpf = request.args.get('cpf', '')
    client_tuple = get_client_info(client_cpf)
    form = AddClientForm()

    form.cpf.data = client_tuple[0]
    form.name.data = client_tuple[1]
    form.surname.data = client_tuple[2]
    form.birthday.data = client_tuple[3]

    rentals = get_rentals_by_client(client_cpf)
    purchases = get_purchases_by_client(client_cpf)
    reservations = get_reservations_by_client(client_cpf)

    return render_template('clients/view_client.html', form=form, rentals=rentals, purchases=purchases, reservations=reservations)
