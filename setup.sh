python3 -m venv .venv
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Trying Windows setup..."
    python -m venv .venv
    .venv\\Scripts\\activate.bat
    if [ $? -ne 0 ]; then
        echo "Virtual environment couldn't be created. See errors above. Exiting."
        exit $?
    fi
    pip3 install -r requirements.txt
    python flaskapp/transform.py
    python runservers.py
fi

pip3 install -r requirements.txt
python3 flaskapp/transform.py
python3 runservers.py
