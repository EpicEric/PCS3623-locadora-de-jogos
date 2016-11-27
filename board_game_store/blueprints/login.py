from board_game_store.db.access import validate_login
from board_game_store.models.user import User
from flask import Blueprint, flash, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_blueprint = Blueprint('login', __name__, template_folder='templates')


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
            user = User(cpf)
            login_user(user)
            return redirect("/")
    return render_template('login.html', form=form, invalid_login=invalid_login)


@login_blueprint.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect("/")
