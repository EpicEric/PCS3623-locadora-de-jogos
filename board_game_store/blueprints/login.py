from board_game_store.db.access import validate_login
from board_game_store.models.user import User
from flask import Blueprint, flash, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user

login_blueprint = Blueprint('login', __name__, template_folder='templates')


@LoginManager.user_loader
def user_loader(cpf):
    return User(cpf)


@LoginManager.request_loader
def request_loader(request):
    cpf = request.form.cpf.data
    password = request.form.password.data
    user = User()
    user.id = cpf
    user.is_authenticated = validate_login(cpf, password)
    return user


@LoginManager.unauthorized_handler
def unauthorized_handler():
    form = AddLoginForm()
    invalid_login = True
    return render_template('login.html', form=form, invalid_login=invalid_login)


class AddLoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    form = AddLoginForm()
    invalid_login = False
    if form.validate_on_submit():
        cpf = form.cpf.data
        password = form.password.data
        valid_login = validate_login(form.cpf.data, form.password.data)
        invalid_login = not valid_login
        if valid_login:
            user = User()
            user.id = cpf
            login_user(user)
            return redirect("/")
    return render_template('login.html', form=form, invalid_login=invalid_login)


@login_blueprint.route('/logout')
def logout_page():
    form = AddLoginForm()
    logout_user()
    return render_template('login.html', form=form)
