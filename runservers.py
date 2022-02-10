import json
import logging
import multiprocessing as mp
import platform
import threading as th

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

    # Use multiprocessing on Linux as forking is supported
    if platform.system() == "Linux":
        multi = mp.Process

    # Multithreading for MacOS and Windows
    else:
        multi = th.Thread

    flask_process = multi(target=serve, args=(flaskapp.app,), kwargs=flask_kwargs)
    dash_process = multi(target=serve, args=(dashapp.server,), kwargs=dash_kwargs)

    logging.basicConfig(level=logging.INFO)

    flask_process.start()
    dash_process.start()
