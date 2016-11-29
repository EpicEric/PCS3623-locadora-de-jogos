from board_game_store.db.access import add_employee, get_all_employee_names, get_employee_info
from board_game_store.models.employee import Employee
from flask import Blueprint, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import login_required

employees_blueprint = Blueprint('employee', __name__, template_folder='templates')


class AddEmployeeForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Sobrenome', validators=[DataRequired()])
    role = StringField('Função', validators=[DataRequired()])
    salary = StringField('Salário', validators=[DataRequired()])
    supervisor = StringField('CPF do supervisor', validators=[DataRequired()])


@employees_blueprint.route('/employees/add-employee', methods=['GET', 'POST'])
@login_required
def add_games_page():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        add_employee(Employee(form.cpf.data, form.password.data, form.name.data, form.surname.data,
                              form.role.data, form.salary.data, form.supervisor.data))
        return redirect('success')
    return render_template('employees/add_employee.html', form=form)


@employees_blueprint.route('/employees/list-employees')
@login_required
def list_employees_page():
    employee_list = get_all_employee_names()
    form = AddEmployeeForm()
    return render_template('employees/list_employees.html', employee_list=employee_list, form=form)


@employees_blueprint.route('/employees/view-employee')
@login_required
def view_client_page():
    employee_cpf = request.args.get('cpf', '')
    employee_tuple = get_employee_info(employee_cpf)

    form = AddEmployeeForm()

    form.cpf.data = employee_tuple[0]
    form.name.data = employee_tuple[1]
    form.surname.data = employee_tuple[2]
    form.role.data = employee_tuple[3]
    form.salary.data = employee_tuple[4]
    form.supervisor.data = employee_tuple[5]

    return render_template('employees/view_employee.html', form=form)
