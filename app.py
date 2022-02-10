from flask import Flask, jsonify

import database
from models import Assay, Compound


app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
mydb = database.DEFAULT_SQLITE_DB


@app.route("/api/compounds", methods=["GET"])
def api_compounds():
    with database.connect_to_sqlite(mydb) as session:
        compounds = session.query(Compound).all()
        return jsonify(compounds)


@app.route("/api/compound/<compound_id>", methods=["GET"])
def api_compound(compound_id: str):
    with database.connect_to_sqlite(mydb) as session:
        compound = (
            session.query(Compound)
            .filter(Compound.compound_id == compound_id)
            .one_or_none()
        )
        return jsonify(compound)


@app.route("/api/assays", methods=["GET"])
def api_assays():
    with database.connect_to_sqlite(mydb) as session:
        assays = session.query(Assay).all()
        return jsonify(assays)


@app.route("/api/assay/<result_id>", methods=["GET"])
def api_assay(result_id: str):
    with database.connect_to_sqlite(mydb) as session:
        assay = session.query(Assay).filter(Assay.result_id == result_id).one_or_none()
        return jsonify(assay)


@app.route("/")
def links():
    return (
        "<a href='api/compounds'>Compounds</a>"
        " | "
        "<a href='api/assays'>Assays</a>"
    )


if __name__ == "__main__":
    app.run()
