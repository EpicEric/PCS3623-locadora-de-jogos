from flask import Flask, render_template
import dao

app = Flask(__name__)


@app.route('/')
def root_page():
    return render_template('main_menu.html')
