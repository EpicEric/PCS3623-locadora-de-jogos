from blueprints.clients import clients_blueprint
import config
from flask import Flask, render_template

app = Flask(__name__)
config.load(app)
app.secret_key = config.get('secret-key')
app.register_blueprint(clients_blueprint)


@app.route('/')
def root_page():
    return render_template('main_menu.html')


@app.route('/success')
def success_page():
    return render_template('success.html')
