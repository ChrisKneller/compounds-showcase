from contextlib import contextmanager
import os
import sqlalchemy as db
import sqlalchemy.orm as orm

# Relative location changes depending on how we call this file
if __name__ in ["__main__", "database"]:
    DEFAULT_SQLITE_DB = "compound_assay"
elif __name__ in ["flaskapp.database"]:
    DEFAULT_SQLITE_DB = os.path.join("flaskapp", "compound_assay")


@contextmanager
def connect_to_sqlite(db_name: str) -> orm.session.Session:
    """
    Connect to the sqlite db at db_name

    Args:
        db_name (str): the name of the sqlite db without the .sqlite extension
    """
    engine = db.create_engine(f"sqlite:///{db_name}.sqlite")
    Session = orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:  # noqa (bare except recommended here in sqlalchemy docs)
        session.rollback()
        raise
    finally:
        session.close()
