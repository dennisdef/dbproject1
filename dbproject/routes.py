from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from dbproject import db, app
from dbproject.forms import *

@app.route("/", methods=['GET', 'POST'])
def index():
    searchprojectform = SearchProjectForm()
    if(request.method == 'POST'):
        new_search = searchprojectform.__dict__
        query = "select p.project_id, p.title from project p inner join executive e on p.ex_id = e.ex_id"
        if((new_search['start_date'].data != None) or (new_search['end_date'].data != None) or (new_search['length'].data != '0') 
            or (new_search['executive'].data != '0')):
            query += " where"
            query1 =""
            if(new_search['start_date'].data != None):
                query1 = " p.start_date >= '" + new_search['start_date'].data.strftime("%Y-%m-%d") + "'"
            if(new_search['end_date'].data != None):
                if(query1 != ""):
                    query1 += " and"
                query1 += " p.end_date <= '" + new_search['end_date'].data.strftime("%Y-%m-%d") + "'"
            if(new_search['length'].data != '0'):
                if(query1 != ""):
                    query1 += " and"
                query1 += " TIMESTAMPDIFF(year, p.start_date, p.end_date) = " + new_search['length'].data 
            if (new_search['executive'].data != '0'):
                if(query1 != ""):
                    query1 += " and"
                query1 += " e.ex_id = " + new_search['executive'].data
            query += query1 
        try:
            query += " order by p.title"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template('show_projects.html', res=res)
        except Exception as e:
            flash(str(e), "danger")

    try:
        cur = db.connection.cursor()
        cur.execute("select ex_id, name from executive order by name")
        column_names = [i[0] for i in cur.description]
        exs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        executives = [('0','-')] +[(e.get('ex_id'), e.get('name')) for e in exs]
        searchprojectform.executive.choices = executives
        return render_template('index.html',
                            pageTitle="Home", form = searchprojectform)
    except Exception as e:
        flash(str(e), "danger")
        return render_template('index.html',
                            pageTitle="Home", form = searchprojectform)

@app.route("/show_project/<id>")
def show_project(id):
    try:
        cur = db.connection.cursor()
        cur.execute("select * from project where project_id = " + id)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("""select concat(r.first_name, ' ', r.last_name) as name from researcher inner join works on w.r_id = r.r_id
                    inner join project on p.project_id = w.project_id where p.project_id = """ + id)
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('show_project.html', res=res, researchers = researchers)
    except Exception as e:
        flash(str(e), "danger")
        return render_template('index.html')

@app.route("/import_researchers/<organisation_id>")
def import_researchers(organisation_id):
    cur = db.connection.cursor()
    cur.execute("select r.r_id, concat(r.first_name, ' ',r.last_name) as name from researcher r where organisation_id = '{}' order by r.first_name ".format(organisation_id))
    column_names = [i[0] for i in cur.description]
    rs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    researchers = [{'id': r['r_id'], 'name': r['name']} for r in rs]
    return jsonify(researchers)

@app.route("/statistics")
def statistics():
    return render_template('statistics.html')

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/add_project", methods = ["GET", "POST"])
def add_project():
    projectform = ProjectForm()
    if(request.method == "POST" ):#and projectform.validate_on_submit()):
        newProject = projectform.__dict__
        researchers = [int(i) for i in request.form.getlist('researchers')]
        evaluator =  newProject['evaluator'].data
        if evaluator in researchers:
            flash("Evaluator cannot be a researcher in the project", "danger")
            return render_template('add_project.html', form=projectform)
        cur = db.connection.cursor()
        cur.execute("SELECT max(project_id) + 1 as project_id from project")
        n = cur.fetchone()[0]
        query = "INSERT INTO project (id,title, summary, start_date, end_date, amount, grade, evaluation_date, evaluator_id, ex_id, program_id, organisation_id, r_id) values ({}, '{}', '{}', '{}', '{}', {}, {}, '{}', {}, {}, {}, {}, {})".format(
         n, newProject['title'].data, newProject['summary'].data, newProject['start_date'].data, newProject['end_date'].data, newProject['amount'].data, newProject['grade'].data, 
        newProject['evaluation_date'].data, newProject['evaluator'].data, newProject['executive'].data, newProject['program'].data, newProject['organisation'].data, request.form['lead_researcher'])
        cur.execute(query)
        for r in researchers:
            cur.execute("insert into works (project_id, r_id) values ({}, {})".format(n, r))
        if newProject['lead_researcher'] in researchers:
            cur.execute("insert into works (project_id, r_id) values ({}, {})".format(n, newProject['lead_researcher']))

        cur.execute("insert into project_science_field (project_id, field_id) values ({}, {})".format(n, newProject['science_field1'].data))
        if newProject['science_field2'].data != 0:
            cur.execute("insert into project_science_field (project_id, field_id) values ({}, {})".format(n, newProject['science_field2'].data))
        db.connection.commit()
        cur.close()
        flash("Project added successfully", "success")
        return render_template('add_project.html', form = projectform)

    cur = db.connection.cursor()
    cur.execute("select program_id, name from program order by name")
    column_names = [i[0] for i in cur.description]
    pr = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.execute("select organisation_id, name from organisation order by name")
    column_names = [i[0] for i in cur.description]
    org = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.execute("select r_id, concat(first_name, ' ', last_name) as name from researcher order by first_name")
    column_names = [i[0] for i in cur.description]
    rs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.execute("select ex_id, name from executive order by name")
    column_names = [i[0] for i in cur.description]
    exs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.execute("select field_id, name from science_field order by name")
    column_names = [i[0] for i in cur.description]
    sfs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    science_fields = [('0','-')] + [(s['field_id'], s['name']) for s in sfs]
    programs = [('0','-')] + [(p.get('program_id'), p.get('name')) for p in pr]
    organisations = [('0','-')] + [(o.get('organisation_id'), o.get('name')) for o in org]
    researchers = [('0','-')] +[(r.get('r_id'), r.get('name')) for r in rs]
    executives = [('0','-')] +[(e.get('ex_id'), e.get('name')) for e in exs]
    projectform.science_field1.choices = projectform.science_field2.choices = science_fields
    projectform.program.choices = programs
    projectform.organisation.choices = organisations
    projectform.evaluator.choices = researchers
    projectform.executive.choices = executives
    return render_template('add_project.html', form = projectform)

@app.route("/add_program", methods=["GET", "POST"])
def add_program():
    programform = ProgramForm()
    if(request.method == "POST" and programform.validate_on_submit()):
        newProgram = programform.__dict__
        query = "INSERT INTO program(name, address) VALUES ('{}', '{}');".format(newProgram['name'].data, newProgram['address'].data)
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Program inserted successfully", "success")
        return redirect(url_for("index"))
    return render_template('add_program.html', form = programform)

@app.route("/add_organisation", methods=["GET", "POST"])
def add_organisation():
    projectform = OrganisationForm()
    if(request.method == "POST"):  ##projectform.validate_on_submit()):
        newOrganisation = projectform.__dict__        
        query = "INSERT INTO organisation(name, abbr, postal_code, street, city, street_number) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(newOrganisation['name'].data, 
                newOrganisation['abbr'].data, newOrganisation['postal_code'].data, newOrganisation['street'].data,
                newOrganisation['city'].data, newOrganisation['street_number'].data)
        
        cur = db.connection.cursor()
        cur.execute(query)

        cur = db.connection.cursor()
        cur.execute("SELECT LAST_INSERT_ID()")
        id = cur.fetchone()[0]
        cur.execute("insert into phone (organisation_id, phone) values ({}, {})".format(id, newOrganisation['phone'].data))
        if newOrganisation['type'].data == 'Company':
            cur.execute("insert into company(organisation_id, equity) values ({}, {})".format(id, newOrganisation['equity'].data))
        if newOrganisation['type'].data == 'University':
            cur.execute("insert into university(organisation_id, budget_me) values ({}, {})".format(id, newOrganisation['equity'].data))
        if newOrganisation['type'].data == 'Research Center':
            cur.execute("insert into company(organisation_id, budget_me, budget_pa) values ({}, {}, {})".format(id, newOrganisation['equity'].data, newOrganisation['equity'].data))
        db.connection.commit()
        cur.close()

        flash("Organisation inserted successfully", "success")
        return render_template('add_organisation.html', form = projectform)

    return render_template('add_organisation.html', form = projectform)

@app.route("/add_researcher", methods=["GET", "POST"])
def add_researcher():
    projectform = ResearcherForm()
    if(request.method == "POST" and projectform.validate_on_submit()):
        newResearcher = projectform.__dict__
        query = "INSERT INTO researcher(first_name, last_name, birth_date, sex, start_date, organisation_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(
                newResearcher['first_name'].data, newResearcher['last_name'].data, newResearcher['birth_date'].data, newResearcher['sex'].data,
                newResearcher['start_date'].data, newResearcher['organisation'].data)
        cur = db.connection.cursor()
        cur.execute(query)

        db.connection.commit()
        cur.close()
        flash("Researcher inserted successfully", "success")
        return render_template('add_researcher.html', form = projectform)

    cur = db.connection.cursor()
    cur.execute("select organisation_id, name from organisation order by name")
    column_names = [i[0] for i in cur.description]
    org = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    organisations = [('0','-')] + [(o.get('organisation_id'), o.get('name')) for o in org]
    projectform.organisation.choices = organisations
    return render_template('add_researcher.html', form = projectform)

@app.route("/add_executive", methods=["GET", "POST"])
def add_executive():
    projectform = ExecutiveForm()
    if(request.method == "POST" and projectform.validate_on_submit()):
        newExecutive = projectform.__dict__
        query = "INSERT INTO executive(name) VALUES ('{}');".format(newExecutive['name'].data)

        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Executive inserted successfully", "success")
        return render_template('add_executive.html', form = projectform)
    return render_template('add_executive.html', form = projectform)


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
    cur.execute("""select r.r_id ,r.first_name, r.last_name, count(r.r_id) as r_number 
                   from researcher r inner join works w on w.r_id = r.r_id 
                   inner join project p on p.project_id = w.project_id
                   WHERE (TIMESTAMPDIFF(year, r.birth_date,CURDATE()) < 40) and p.end_date > CURDATE()
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

@app.route("/show_all_researchers")
def show_all_researchers():
    cur = db.connection.cursor()
    cur.execute("""select r.r_id as id, concat(r.first_name, ' ', r.last_name) as name from researcher r""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    return render_template("show_all.html", res = res)

@app.route("/show_all_executives")
def show_all_executives():
    cur = db.connection.cursor()
    cur.execute("""select e.ex_id as id, e.name from executive e""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    return render_template("show_all_executives.html", res = res)

@app.route("/show_all_programs")
def show_all_programs():
    cur = db.connection.cursor()
    cur.execute("""select program_id as id, name from program""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    return render_template("show_all_programs.html", res = res)

@app.route("/show_all_organisations")
def show_all_organisations():
    cur = db.connection.cursor()
    cur.execute("""select o.organisation_id as id, o.name from organisation o;""")
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    return render_template("show_all_organisations.html", res = res)

@app.route("/delete_researcher/<id>")
def delete_researcher(id):
    cur = db.connection.cursor()
    cur.execute("delete from researcher where r_id = {}".format(id))
    cur.execute("delete from works where r_id = {}".format(id))
    db.connection.commit()
    cur.close()
    flash("Researcher deleted", "success")
    return redirect(url_for("show_all_researchers"))

@app.route("/delete_program/<id>")
def delete_program(id):
    cur = db.connection.cursor()
    cur.execute("delete from program where program_id = {}".format(id))
    db.connection.commit()
    cur.close()
    flash("Program deleted", "success")
    return redirect(url_for("show_all_programs"))

@app.route("/delete_organisation/<id>")
def delete_organisation(id):
    cur = db.connection.cursor()
    cur.execute("delete from organisation where organisation_id = {}".format(id))
    db.connection.commit()
    cur.close()
    flash("Organisation deleted", "success")
    return redirect(url_for("show_all_organisations"))

@app.route("/delete_executive/<id>")
def delete_executive(id):
    cur = db.connection.cursor()
    cur.execute('select project_id from project where ex_id = {}'.format(id))
    res = cur.fetchall()
    if res == []:
        cur.execute("delete from executive where ex_id = {}".format(id))
        db.connection.commit()
        cur.close()
        flash("Executive deleted", "success")
        return redirect(url_for("show_all_executives"))
    else:
        cur.close()
        flash("Executive can't be deleted, he/she/it is responsible for a project", "danger")
        return redirect(url_for("show_all_executives"))

@app.route("/update_researcher/<id>" , methods=["GET", "POST"])
def update_researcher(id):
    researcherForm = ResearcherForm()
    if(request.method == "POST" and researcherForm.validate_on_submit()):
        update_researcher = researcherForm.__dict__
        cur = db.connection.cursor()
        print
        cur.execute("update researcher set first_name = '{}', last_name = '{}', birth_date = '{}', sex = '{}', start_date = '{}', organisation_id = {} where r_id = {}".format(
            update_researcher['first_name'].data, update_researcher['last_name'].data, update_researcher['birth_date'].data, 
            update_researcher['sex'].data, update_researcher['start_date'].data, update_researcher['organisation'].data, id
        ))
        if(update_researcher['organisation'] != request.form['o_id']):
            cur.execute("delete from works where r_id = {}".format(id))
        db.connection.commit()
        cur.close()
        flash("Researcher updated", "success")
        return redirect(url_for("show_all_researchers"))
        
    cur = db.connection.cursor()
    cur.execute("select * from researcher where r_id = {}".format(id))
    column_names = [i[0] for i in cur.description]
    res = dict(zip(column_names, cur.fetchone()))
    researcherForm.first_name.data = res.get("first_name")
    researcherForm.last_name.data = res.get("last_name")
    researcherForm.birth_date.data = res.get("birth_date")
    researcherForm.sex.data = res.get("sex")
    researcherForm.start_date.data = res.get("start_date")
    cur.execute("select organisation_id, name from organisation order by name")
    column_names = [i[0] for i in cur.description]
    org = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    organisations = [('0','-')] + [(o.get('organisation_id'), o.get('name')) for o in org]
    researcherForm.organisation.choices = organisations
    cur.close()
    return render_template("add_researcher.html", form=researcherForm, r_id=id, o_id = res.get("organisation_id"))

@app.route("/update_executive/<id>" , methods=["GET", "POST"])
def update_executive(id):    
    executiveform = ExecutiveForm()
    if(request.method == "POST" and executiveform.validate_on_submit()):
        update_executive = executiveform.__dict__
        cur = db.connection.cursor()
        cur.execute("update executive set name = '{}' where ex_id = {}".format(
            update_executive['name'].data, id
        ))
        db.connection.commit()
        cur.close()
        flash("Executive updated", "success")
        return redirect(url_for("show_all_executives"))
    
    cur = db.connection.cursor()
    cur.execute("select * from executive where ex_id = {}".format(id))
    column_names = [i[0] for i in cur.description]
    res = dict(zip(column_names, cur.fetchone()))
    cur.close()
    executiveform.name.data = res.get("name")
    return render_template("add_executive.html", form=executiveform, id=id)


@app.route("/update_program/<id>" , methods=["GET", "POST"])
def update_program(id):    
    programform = ProgramForm()
    if(request.method == "POST" and programform.validate_on_submit()):
        update_program = programform.__dict__
        cur = db.connection.cursor()
        cur.execute("update program set name = '{}', address = '{}' where program_id = {}".format(
            update_program['name'].data, update_program['address'].data, id
        ))
        db.connection.commit()
        cur.close()
        flash("Program updated", "success")
        return redirect(url_for("show_all_programs"))
    
    cur = db.connection.cursor()
    cur.execute("select * from program where program_id = {}".format(id))
    column_names = [i[0] for i in cur.description]
    res = dict(zip(column_names, cur.fetchone()))
    cur.close()
    programform.name.data = res.get("name")
    programform.address.data = res.get("address")
    return render_template("add_program.html", form=programform, id=id)

@app.route("/update_organisation/<id>" , methods=["GET", "POST"])
def update_organisation(id):
    organisationForm = OrganisationForm()
    if(request.method == "POST" and organisationForm.validate_on_submit()):
        update_organisation = organisationForm.__dict__
        cur = db.connection.cursor()
        cur.execute("update organisation set name = '{}', abbr = '{}', postal_code = '{}', street = '{}', city = '{}', street_number = {} where organisation_id = {}".format(
            update_organisation['name'].data, update_organisation['abbr'].data, update_organisation['postal_code'].data, update_organisation['street'].data, 
            update_organisation['city'].data, update_organisation['street_number'].data, id
        ))
        db.connection.commit()
        cur.close()
        flash("Organisation updated", "success")
        return redirect(url_for("show_all_organisations"))
        
    cur = db.connection.cursor()
    cur.execute("select * from organisation where organisation_id = {}".format(id))
    column_names = [i[0] for i in cur.description]
    res = dict(zip(column_names, cur.fetchone()))
    cur.close()
    organisationForm.name.data = res.get("name")
    organisationForm.abbr.data = res.get("abbr")
    organisationForm.postal_code.data = res.get("postal_code")
    organisationForm.street.data = res.get("street")
    organisationForm.street_number.data = res.get("street_number")
    organisationForm.city.data = res.get("city")
    
    return render_template("add_organisation.html", form=organisationForm)