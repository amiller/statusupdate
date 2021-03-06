import MySQLdb
import simplejson as json
import os


with open('config.json', 'r') as f:
    config = json.load(f)


def connect():
    global conn
    conn = MySQLdb.connect(db=config['db'],
                           user=config['user'],
                           passwd=config['pw'])
    return conn
connect()


def cursor():
    global conn
    try:
        conn.ping()
        return conn.cursor()
    except MySQLdb.OperationalError:
        return connect().cursor()


def random_template():
    conn = connect()
    c = conn.cursor()
    c.execute("""
        SELECT template FROM status_templates
        WHERE id >= (SELECT FLOOR(MAX(id)) * RAND() FROM status_templates)
        ORDER BY id LIMIT 1;""")
    template, = c.fetchone()
    return template

    
if __name__ == "__main__":
    print random_template()
