from .blueprints.login import login_blueprint
from .blueprints.clients import clients_blueprint
from .blueprints.employees import employees_blueprint
from .blueprints.games import games_blueprint
from .blueprints.rooms import rooms_blueprint
from .db.access import NoDBElementError
from .models.user import User
import os
import board_game_store.config as config
from flask import flash, Flask, render_template, redirect, send_from_directory
from flask_login import LoginManager, login_required

app = Flask(__name__)
config.load(app)
app.secret_key = config.get('secret-key')
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(login_blueprint)
app.register_blueprint(clients_blueprint)
app.register_blueprint(employees_blueprint)
app.register_blueprint(games_blueprint)
app.register_blueprint(rooms_blueprint)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@login_manager.user_loader
def user_loader(cpf):
    return User(cpf)


# @login_manager.request_loader
# def request_loader(request):
#     cpf = request.form.cpf.data
#     password = request.form.password.data
#     user = User(cpf)
#     user.is_authenticated = validate_login(cpf, password)
#     return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login")


@app.route('/')
@login_required
def root_page():
    return render_template('main_page.html')


@app.route('/success')
def success_page():
    return render_template('success.html')


@app.route('/error')
def error_page():
    return render_template('error.html'), 400


@app.errorhandler(NoDBElementError)
def handle_db_error(error):
    import traceback
    flash('Erro no banco de dados: {}\n{}'.format(error, traceback.format_exc()))
    return redirect('/error')


@app.errorhandler(RuntimeError)
def handle_runtime_error(error):
    import traceback
    flash('Erro: {}\n{}'.format(error, traceback.format_exc()))
    return redirect('/error')
