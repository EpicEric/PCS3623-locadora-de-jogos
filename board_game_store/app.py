from .blueprints.login import login_blueprint
from .blueprints.clients import clients_blueprint
from .blueprints.employees import employees_blueprint
from .blueprints.games import games_blueprint
from .blueprints.rooms import rooms_blueprint
import board_game_store.config as config
from flask import Flask, render_template
from flask_login import LoginManager

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


@app.route('/')
def root_page():
    return render_template('main_page.html')


@app.route('/success')
def success_page():
    return render_template('success.html')


@app.route('/error')
def error_page():
    return render_template('error.html')
