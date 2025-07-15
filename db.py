import psycopg2
import psycopg2.extras

def get_db_connection():
    return psycopg2.connect(
        dbname='flaskblog',
        user='flaskuser',
        password='1234',
        host='localhost',
        cursor_factory=psycopg2.extras.RealDictCursor  
    )
