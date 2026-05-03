import os
import psycopg2
import psycopg2.extras


def _normalize_database_url(url):
    """Render/Heroku often use postgres://; psycopg2 expects postgresql://."""
    if url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return psycopg2.connect(
            _normalize_database_url(database_url),
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
    return psycopg2.connect(
        dbname=os.environ.get('PGDATABASE', 'flaskblog'),
        user=os.environ.get('PGUSER', 'flaskuser'),
        password=os.environ.get('PGPASSWORD', '1234'),
        host=os.environ.get('PGHOST', 'localhost'),
        port=os.environ.get('PGPORT', '5432'),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
