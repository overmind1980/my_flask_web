from flask import Flask,render_template,request,redirect,session,Blueprint
from db import pool
import psycopg
import traceback
from random import randint

app_user = Blueprint("user", __name__)

@app_user.route('/user/')
def user():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            limit = 10
            offset = 0
            pages = list(range(0, 10))
            sql = "SELECT * FROM login" \
                        + " ORDER BY username " \
                        + " LIMIT " + str(limit) \
                        + " OFFSET " + str(offset)
            cur.execute(sql)
            records = cur.fetchall()
            cur.close()
        conn.close()
    return render_template("user_manager.html", l = records, pages= pages)

@app_user.route("/user/del", methods=['POST', 'GET'])
def del_user():
    username = request.form["d_un"]
    user_order = request.form.get("user_order")
    page = int(request.form.get("page"))
    first_page = int(page)
    page_size = request.form.get("page_size")
    print("uname===========",username)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                sql = """DELETE FROM login WHERE username=%s"""
                print("sql=========",sql)
                t = (username,)
                cur.execute(sql,t)
                conn.commit()
                cur.close()
                conn.close()
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return  username + " deletion failed"
            else:
                return redirect("/user")

@app_user.route("/user/dels", methods=['POST', 'GET'])
def del_users():
    users = request.form.getlist("users")
    user_order = request.form.get("user_order")
    page = int(request.form.get("page"))
    first_page = int(page)
    page_size = request.form.get("page_size")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                sql = """DELETE FROM login WHERE username=%s"""
                for user in users:
                    t = (user,)
                    cur.execute(sql,t)
                conn.commit()
                cur.close()
                conn.close()
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return  username + " already exists"
            else:
                return redirect("/user")

@app_user.route("/user/add", methods=['POST', 'GET'])
def user_add():
    username = request.form["username"]
    password = request.form["password"]
    print(username)
    conninfo = "postgres://postgres:oeasypg@localhost:5432/oeasydb"
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            try:
                sql = "INSERT INTO login(username, password) VALUES(%s, %s)"""
                t = (username,password)
                cur.execute(sql,t)
                conn.commit()
            except Exception:
                print(traceback.print_exc())
                return "add " + username + " failed!"
            else:
                return redirect("/user")


def get_random_str():
    s = ""
    for i in range(10):
        s += chr(randint(0x61,0x61+27))
    return s

@app_user.route("/user/add_users", methods=['POST', 'GET'])
def add_users():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                for i in range(200):
                    sql = "INSERT INTO login(username, password) VALUES(%s, %s)"
                    username = get_random_str()
                    password = get_random_str()
                    l = [username, password]
                    print("l==========", l)
                    cur.execute(sql,l)
                conn.commit()
                cur.close()
                conn.close()
                redirect("/user")
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return  "add user failed!"
            else:
                return redirect("/user")

@app_user.route("/user/prepareUpdate", methods=['POST', 'GET'])
def prepare_update():
    username = request.args.get("username")
    print("now in prepare update" + username)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                sql = "SELECT * FROM login WHERE username=%s"
                t = (username,)
                detail = cur.execute(sql,t).fetchone()
                user = detail[0]
                password = detail[1]
                cur.close()
                conn.close()
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return  "failed to get " + username
            else:
                return render_template("user_detail.html", user = user, password = password)

@app_user.route("/update", methods=['POST', 'GET'])
def update():
    old_username = request.form.get("old_username")
    username = request.form.get("username")
    password = request.form.get("password")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                sql = """UPDATE login SET username=%s,password=%s where username=%s"""
                t = (username,password,old_username)
                cur.execute(sql,t)
                conn.commit()
                cur.close()
                conn.close()
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return "update " + username + "failed!"
            else:
                return redirect("/user")

@app_user.route("/user/search", methods=['POST', 'GET'])
def search():
    username = request.form.get("s_usr")
    user_order = request.form.get("user_order")
    page = int(request.form.get("page"))
    first_page = int(page)
    page_size = request.form.get("page_size")
    print(page_size,"-------------")
    if page_size == None or page_size == "":
        page_size = "10"
    username_pattern = "%" + username + "%"
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                sql = "SELECT count(*) FROM login WHERE username LIKE %s"
                t = (username_pattern,)
                cur.execute(sql,t)
                count = cur.fetchone()
                count = int(count[0])
                print("count====",count)
                if count <= 100:
                    first_page = 0
                    last_page = count // int(page_size)
                else:
                    if page < 5:
                        first_page = 0
                        last_page = 10
                    elif count//10 - page < 5:
                        last_page = count//10 + 1
                        first_page = last_page - 10
                    else:
                        first_page = page - 5
                        last_page = page + 4
                sql = "SELECT * FROM login WHERE username LIKE %s ORDER BY username " + user_order + " LIMIT " + page_size + " OFFSET " + str(int(page) * 10)
                t = (username_pattern,)
                cur.execute(sql,t)
                records = cur.fetchall()
                cur.close()
                conn.close()
            except Exception:
                print(traceback.print_exc())
                cur.close()
                conn.close()
                return  username + " already exists"
            print(page,"====")
            return render_template("user_manager.html", l = records, s_user = username,user_order = user_order, pages=list(range(first_page, last_page)),current_page = page,page_size = page_size)
