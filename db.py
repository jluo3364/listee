import sqlite3

def open():
    conn = sqlite3.connect('static/lists.db')
    return (conn, conn.cursor())

def close(conn, cur):
    cur.close()
    conn.close()

def all_lists():
    conn, cur = open()
    cur.execute("SELECT * FROM lists")
    rows = cur.fetchall()

    lists = []
    for r in rows:
        lists.append(r)
        print(r)
        
    close(conn, cur)
    return lists #array of tuples: id, name

def delete_lists(ids):
    conn, cur = open()
    for i in ids:
        list_table = "l" + str(i)
        print(list_table)
        cur.execute("DROP TABLE IF EXISTS {}".format(list_table))
        cur.execute("DELETE FROM lists WHERE id = (?)", (i, ))
    conn.commit()
    close(conn, cur)

def delete_items(list_name, items):
    conn, cur = open()
    table_name = list_table_name(list_name)
    for i in items:
        cur.execute("DELETE FROM {} WHERE item = ?".format(table_name), (i, ))
    conn.commit()
    close(conn, cur)
    return get_items(list_name)

def insert_item(list_name, item):
    conn, cur = open()
    table_name = list_table_name(list_name)
    cur.execute("INSERT INTO {} (item) VALUES (?)".format(table_name), (item, ))
    conn.commit()
    close(conn, cur)

def get_items(list_name):
    conn, cur = open()
    table_name = list_table_name(list_name)
    
    sql = "SELECT item FROM {}"
    cur.execute(sql.format(table_name))
    res = cur.fetchall()
    items = []
    for r in res:
        items.append(r[0])
    close(conn, cur)
    return items

def create_table(list_name):
    conn, cur = open()
    cur.execute("SELECT id FROM lists ORDER BY id DESC LIMIT 1")
    id = cur.fetchone()
    if id:
        id = id[0] + 1
    else:
        id =1
    cur.execute(" INSERT INTO lists (id, list_name) VALUES (?,?)", (id, list_name) )
    sql = "CREATE TABLE IF NOT EXISTS {} (item TEXT NOT NULL)"
    name = f"l{id}"
    cur.execute(sql.format(name))  #name = "l"+list_id
    conn.commit()
    close(conn, cur)
    return name

def list_table_name(list_name):
    conn, cur = open()
    cur.execute("SELECT id FROM lists WHERE list_name = (?)", (list_name, ))
    id = cur.fetchone()[0]
    close(conn, cur)
    return f"l{id}"

def num_lists():
    conn, cur = open()
    cur.execute("SELECT COUNT(*) FROM lists")
    num, = cur.fetchone()
    close(conn, cur)
    return num