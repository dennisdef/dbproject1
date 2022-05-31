from flask import Flask, render_template
from flask_mysqldb import MySQL
from dbproject import db, app


@app.route("/")
def index():
    return render_template('index.html',
            pageTitle = "Home")
    ## cur = db.connection.cursor()
    ##cur.execute("select r_id, first_name, last_name from researcher ")
    ##column_names = [i[0] for i in cur.description]
    ##res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    # cur.close()


@app.route("/executives")
def executives():
    cur = db.connection.cursor()
    cur.execute(
        "select e.name,p.amount from executive e inner join project p on p.ex_id = e.ex_id order by p.amount desc limit 5")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close() 
    return render_template('ex.html',
                        pageTitle = "Executives",
                        executives=res
                           )

@app.route("/under_40")
def under_40():
    cur = db.connection.cursor()
    cur.execute("select r.first_name, r.last_name, count(r.r_id) as r_number from researcher r inner join works w on w.r_id = r.r_id WHERE TIMESTAMPDIFF(year, r.birth_date,CURDATE()) < 40 group by r.r_id order by count(r.r_id) desc")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template('under_40.html',
                        pageTitle = "Researchers under 40",
                        researchers=res
                        )

                        