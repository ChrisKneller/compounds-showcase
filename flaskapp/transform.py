import json
import os
from prefect import task, Flow
import sqlalchemy as db

from flaskapp import database
from flaskapp.models import Assay, Base, Compound


@task
def create_sqlite_tables(db_name: str) -> bool:
    """
    Create tables from models.py in a sqlite db at db_name.

    Args:
        db_name (str): the name of the sqlite db without the .sqlite extension

    Returns:
        bool: True if the function runs without any errors
    """
    engine = db.create_engine(f"sqlite:///{db_name}.sqlite")
    Base.metadata.create_all(engine)
    return True


@task
def extract_compounds_from_json(json_path: str) -> list:
    """
    Read the json file located at json_path and return a list of Compound
    objects based on the contents of the file.

    Args:
        json_path (str): the path to the json file containing compound data

    Returns:
        list: a list of Compound objects
    """
    with open(json_path, "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    compounds = []
    for comp in data:
        assays = [Assay(**assay) for assay in comp["assay_results"]]
        comp["assay_results"] = assays
        compound = Compound(**comp)
        compounds.append(compound)
    return compounds


@task
def add_compounds_to_db(db_name: str, compounds: list) -> bool:
    """
    Given a db name and a list of compounds, add the compounds to the db

    Args:
        db_name (str): the name of the sqlite db
        compounds (list): a list of Compound objects

    Returns:
        bool: True if the function runs without any errors
    """
    for compound in compounds:
        with database.connect_to_sqlite(db_name) as session:
            compound_in_table = (
                session.query(Compound)
                .filter(Compound.compound_id == compound.compound_id)
                .one_or_none()
            )
            if not compound_in_table:
                session.add(compound)
    return True


with Flow("compounds_json_to_sqlite") as flow:
    mydb = database.DEFAULT_SQLITE_DB
    myjson = os.path.join("data", "compounds.json")

    tables_exist = create_sqlite_tables(mydb)
    compounds = extract_compounds_from_json(myjson)
    added = add_compounds_to_db(mydb, compounds, upstream_tasks=[tables_exist])

if __name__ == "__main__":
    flow.run()
