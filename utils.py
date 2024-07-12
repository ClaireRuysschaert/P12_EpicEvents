from constants import DEPARTMENTS_BY_ID

from local_settings import postgresql as settings
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker


def get_engine(user, passwd, host, port, db) -> Engine:
    """
    Get the engine for the database.
    """
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_engine_from_settings() -> Engine:
    """
    Get the engine for the database from the settings.
    """
    required_keys = ["pguser", "pgpasswd", "pghost", "pgport", "pgdb"]
    if not all(key in required_keys for key in settings.keys()):
        raise Exception("Bad config file")

    return get_engine(
        settings["pguser"],
        settings["pgpasswd"],
        settings["pghost"],
        settings["pgport"],
        settings["pgdb"],
    )


Base = declarative_base()


def create_tables(engine: Engine) -> None:
    """
    Create the tables in the database.
    """
    Base.metadata.create_all(engine)


def get_session() -> tuple[Engine, sessionmaker]:
    """
    Get the session for the database.
    """
    engine = get_engine_from_settings()
    create_tables(engine)
    session = sessionmaker(bind=engine)()
    return engine, session


engine, session = get_session()


def is_management_team(department_id: int) -> bool:
    """
    Verifies if the department is management.
    """
    return department_id == DEPARTMENTS_BY_ID["management"]


def is_commercial_team(department_id: int) -> bool:
    """
    Verifies if the department is commercial.
    """
    return department_id == DEPARTMENTS_BY_ID["commercial"]


def is_support_team(department_id: int) -> bool:
    """
    Verifies if the department is support.
    """
    return department_id == DEPARTMENTS_BY_ID["support"]
