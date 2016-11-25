from flask import Flask
import dao


app = Flask(__name__)


@app.route('/')
def get_client_in_room():
    return repr(dao.get_room_reservation())
