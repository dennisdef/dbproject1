from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbproject import db, app
from dbproject.forms import *

@app.route("/")
def index():
    return render_template('index.html',
                           pageTitle="Home")
    ## cur = db.connection.cursor()
    ##cur.execute("select r_id, first_name, last_name from researcher ")
    ##column_names = [i[0] for i in cur.description]
    ##res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    # cur.close()

@app.route("/statistics")
def statistics():
    return render_template('statistics.html')

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/add_project")
def add_project():
    projectform = ProjectForm()
    return render_template('add_project.html', form = projectform)

@app.route("/add_organisation")
def add_organisation():
    projectform = ProjectForm()
    return render_template('add_project.html', form = projectform)

@app.route("/add_program")
def add_program():
    projectform = ProjectForm()
    return render_template('add_project.html', form = projectform)

@app.route("/add_researcher")
def add_researcher():
    projectform = ProjectForm()
    return render_template('add_project.html', form = projectform)

@app.route("/add_executive")
def add_executive():
    projectform = ProjectForm()
    return render_template('add_project.html', form = projectform)


@app.route("/executives")
def executives():
    cur = db.connection.cursor()
    cur.execute(
        """select e.name as executive_name, o.name as organisation_name, sum(p.amount) as total_money 
        from executive e inner join project p on p.ex_id = e.ex_id
        INNER join organisation o on p.organisation_id = o.organisation_id
        inner join company c on o.organisation_id = c.organisation_id
        group by e.name, o.organisation_id order by total_money desc limit 5""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template('ex.html',
                           pageTitle="Executives",
                           executives=res
                           )


@app.route("/under_40")
def under_40():
    cur = db.connection.cursor()
    cur.execute("""select r.first_name, r.last_name, count(r.r_id) as r_number 
                   from researcher r inner join works w on w.r_id = r.r_id 
                   WHERE TIMESTAMPDIFF(year, r.birth_date,CURDATE()) < 40 
                   group by r.r_id order by count(r.r_id) desc""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template('under_40.html',
                           pageTitle="Researchers under 40",
                           researchers=res
                           )


@app.route("/science_fields")
def science_fields():
    cur = db.connection.cursor()
    cur.execute(f"select sf.name, sf.en_name from science_field sf")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template('sfs.html',
                           pageTitle="Science Fields",
                           sfs=res
                           )


@app.route("/science_fields/<sf>")
def science_field(sf):
    cur = db.connection.cursor()
    query = "select * from science_field where en_name = '{}''".format(sf)
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    res = dict(zip(column_names, cur.fetchone()))
    cur.close()

    return render_template('index.html',
                           pageTitle=res.get("name"),
                           test=res.get("en_name")
                           )


@app.route("/con_project_per_year")
def project_per_year():
    cur = db.connection.cursor()
    cur.execute("""SELECT ppy1.name, ppy1.count_projects from
                 project_per_year ppy1 inner join
                 project_per_year ppy2
                 on ppy1.organisation_id = ppy2.organisation_id
                 and ppy1.s_year = ppy2.s_year + 1 """)
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("project_per_year.html",
                           pageTitle="Consecutive projects",
                           ppys=res
                           )


@app.route("/researcher_with_no_del")
def res_with_no_del():
    cur = db.connection.cursor()
    cur.execute("""select CONCAT(r.first_name, ' ', r.last_name) as name, count(w.r_id) as n_projects
                from researcher r inner join works w on r.r_id = w.r_id 
                inner join project p on w.project_id = p.project_id 
                where not exists (SELECT p2.project_id FROM project p2 
                inner join deliverable d on p2.project_id =d.project_id 
                where p.project_id = p2.project_id) 
                GROUP BY r.r_id 
                having count(w.r_id) > 4 order by n_projects desc""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("res_no_del.html",
                           pageTitle="Researchers with no deliverables",
                           rnds=res
                           )

@app.route("/top_scinece_field_couples")
def top_science_field_couple():
    cur = db.connection.cursor()
    cur.execute("""SELECT CONCAT(a.name, " - ", b.name) as field_couple, count(a.project_id) as np from
                science_field_per_project a 
                inner join science_field_per_project b 
                on a.project_id = b.project_id and a.field_id > b.field_id
                group by field_couple 
                ORDER by np desc limit 3""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("top_fields.html",
                           pageTitle="Top science field couples", 
                           top_fields=res)
                           

