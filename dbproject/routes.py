from flask import Flask, render_template
from flask_mysqldb import MySQL
from dbproject import db,app

@app.route("/")
def index():
    cur = db.connection.cursor()
    cur.execute("select r_id, first_name, last_name from researcher ")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template('index.html',
            names = res)


@app.route("/hello")
def hello():
    return ("Hello World!")