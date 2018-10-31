import sqlite3
import datetime
from shutil import copy


def get_db_connection():
    conn = sqlite3.Connection("data.db")
    c = conn.cursor()
    return (conn, c)

def auth(n,p):
    conn, c = get_db_connection()
    try:
        c.execute("select pass, role from users where name=?",(n,))
        res = c.fetchone()
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    password, role = res
    if password == p:
        return role
    return None
    
def get_devices_list():
    conn, c = get_db_connection()
    try:
        c.execute("select name, id from devices")
        res = c.fetchall()
        d = [a[0] for a in res]
        i = [a[1] for a in res]
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    return [d, i]


def get_tasks_list(id):
    conn, c = get_db_connection()
    try:
        c.execute("select title, id from tasks where d_id=?", (id,))
        res = c.fetchall()
        t = [a[0] for a in res]
        i = [a[1] for a in res]
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    return [t, i]

def get_archived_tasks():
    conn, c = get_db_connection()
    try:
        c.execute("select id, title from archived_tasks")
        res = c.fetchall()
        i = [a[0] for a in res]
        t = [a[1] for a in res]
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    return [t, i]

def get_archived_task(id):
    conn, c = get_db_connection()
    try:
        c.execute("select * from archived_tasks where id=?",(id,))
        res = c.fetchone()
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    return res


def get_comments(t_id):
    conn, c = get_db_connection()
    try:
        c.execute("select comment from tasks where id=?", (t_id,))
        res = c.fetchone()[0]
    except Exception as e:
        res = ""
        print(e)
    conn.commit()
    c.close()
    conn.close()
    print(res)
    return res


def update_comment(t_id, comment):
    conn, c = get_db_connection()
    try:
        print("=>updating comment of {}".format(t_id))
        c.execute("update tasks set comment=? where id=?", (comment, t_id))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def get_device_status(id):
    conn, c = get_db_connection()
    try:
        print("=>gettin status of {}".format(id))
        c.execute("select status from devices where id=?", (id,))
        res = c.fetchone()[0]
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()
    return res


def toggle_status(id, status):
    conn, c = get_db_connection()
    try:
        print("=>toggling status to {} on {}".format(status, id))
        c.execute("update devices set status=? where id=?", (status, id))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def add(value, sql):
    conn, c = get_db_connection()
    try:
        c.execute(sql, (value,))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def edit(value, sql):
    conn, c = get_db_connection()
    try:
        c.execute(sql, (value,))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def delete(sql):
    conn, c = get_db_connection()
    try:
        c.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def del_device(d_id):
    conn, c = get_db_connection()
    try:
        c.execute("delete from devices where id=?", (d_id,))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()


def del_task(d_id):
    conn, c = get_db_connection()
    try:
        c.execute("delete from tasks where d_id=?", (d_id,))
    except Exception as e:
        print(e)
    conn.commit()
    c.close()
    conn.close()

def backup(name=None):
    if name == None:
        name = datetime.datetime.now().strftime("%d'%m'%Y %H-%M")
    path = "./backup/{}.db".format(name)
    try:
        print(name)
        copy("./data.db", path)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    pass