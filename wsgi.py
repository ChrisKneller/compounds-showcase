import json
import logging
from multiprocessing import Process
from waitress import serve

from flaskapp import app as flaskapp
from dashapp import dashapp

# Load and set constants
with open("settings.json", "r") as file:
    server_info = json.load(file)

HOST = server_info["host"]
FLASK_PORT = server_info["flask_port"]
DASH_PORT = server_info["dash_port"]

flask_kwargs = {"host": HOST, "port": FLASK_PORT}
dash_kwargs = {"host": HOST, "port": DASH_PORT}

if __name__ == "__main__":

    flask_process = Process(target=serve, args=(flaskapp.app,), kwargs=flask_kwargs)
    dash_process = Process(target=serve, args=(dashapp.server,), kwargs=dash_kwargs)

    logging.basicConfig(level=logging.INFO)

    flask_process.start()
    dash_process.start()
