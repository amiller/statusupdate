import MySQLdb

def connect():
    global conn
    conn = MySQLdb.connect(db='soc1024c_statusupdate02',
                           user='soc1024c_odesk02',
                           passwd='o6kD2D0')

def random_template():
    c = conn.cursor()
    c.execute("""
        SELECT template FROM status_templates
        WHERE id >= (SELECT FLOOR(MAX(id)) * RAND() FROM status_templates)
        ORDER BY id LIMIT 1;""")
    template, = c.fetchone()
    return template
    
if __name__ == "__main__":
    connect()
    print random_template()
