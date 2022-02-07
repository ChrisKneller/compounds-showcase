from flask import Flask, jsonify

from models import Assay, Compound
from transform import connect_to_sqlite

app = Flask(__name__)


@app.route("/compounds")
def api_compounds():
    with connect_to_sqlite("compound_assay") as session:
        compounds = session.query(Compound).all()
        return jsonify(compounds)

@app.route("/compound/<compound_id>")
def api_compound(compound_id: str):
    with connect_to_sqlite("compound_assay") as session:
        compound = (
            session.query(Compound)
            .filter(Compound.compound_id == compound_id)
            .one_or_none()
        )
        return jsonify(compound)

@app.route("/assays")
def api_assays():
    with connect_to_sqlite("compound_assay") as session:
        assays = session.query(Assay).all()
        return jsonify(assays)

@app.route("/assay/<result_id>")
def api_assay(result_id: str):
    with connect_to_sqlite("compound_assay") as session:
        assay = (
            session.query(Assay)
            .filter(Assay.result_id == result_id)
            .one_or_none()
        )
        return jsonify(assay)


@app.route("/")
def hello_world():
    return "Hello, world"
