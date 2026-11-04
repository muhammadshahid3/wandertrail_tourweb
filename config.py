import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _database_uri():
    """Build the DB URL from the DB_* variables.

    DB_ENGINE=mysql       -> AWS RDS MySQL (default, same as before)
    DB_ENGINE=postgresql  -> local Docker Postgres
    URL.create() escapes special characters in the password for us.
    """
    engine = os.environ.get('DB_ENGINE', 'mysql').lower()
    drivers = {
        'mysql': ('mysql+pymysql', '3306'),
        'postgresql': ('postgresql+psycopg2', '5432'),
        'postgres': ('postgresql+psycopg2', '5432'),
    }
    drivername, default_port = drivers.get(engine, drivers['mysql'])
    return URL.create(
        drivername=drivername,
        username=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', default_port)),
        database=os.environ.get('DB_NAME', 'tour_booking'),
    )


class Config:
    """Base configuration. All sensitive values come from environment
    variables, so the same image runs against AWS RDS or a local DB."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me')

    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads

    WTF_CSRF_ENABLED = True
