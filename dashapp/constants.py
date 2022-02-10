import json

# Relative location changes depending on how we call this file
if __name__ == "__main__":
    json_location = "../settings.json"
elif __name__ == "dashapp.constants":
    json_location = "settings.json"

# Load and set constants
with open(json_location, "r") as file:
    server_info = json.load(file)

HOST = server_info["host"]
FLASK_PORT = server_info["flask_port"]
DASH_PORT = server_info["dash_port"]

FLASK_BASE = "http://" + HOST + ":" + FLASK_PORT
DASH_BASE = "http://" + HOST + ":" + DASH_PORT

API_BASE = FLASK_BASE + "/api"
API_COMPOUNDS = API_BASE + "/compounds"
API_SINGLE_COMPOUND = API_BASE + "/compound/{}"
API_ASSAYS = API_BASE + "/assays"
API_SINGLE_ASSAY = API_BASE + "/assay/{}"

COMPOUNDS = DASH_BASE + "/compounds"
SINGLE_COMPOUND = DASH_BASE + "/compound/{}"
ASSAYS = DASH_BASE + "/assays"
SINGLE_ASSAY = DASH_BASE + "/assay/{}"
