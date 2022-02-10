python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 flaskapp/transform.py
python3 runservers.py
