from datetime import date
import decimal
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, NumberRange
from dbproject import db, app

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class ProjectForm(FlaskForm):
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])
    summary = TextAreaField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])
    start_date = DateField(label = "Start Date", default = date.today())
    end_date = DateField(label = "End Date", validators = [DataRequired(message = "End Date is a required field.")])
    amount = DecimalField(places = 2, label = "Amount", validators = [DataRequired(message = "Amount is a required field."), NumberRange(min = 100000, max = 1000000, message = "Amount must be between 100,000 and 1,000,000")])
    grade = DecimalField(places = 1, label= "Grade", validators= [DataRequired(message = "Grade is a required field."), NumberRange(min = 100000, max = 1000000, message = "Amount must be between 100,000 and 1,000,000")])
    evaluation_date = DateField(label= "Evaluation Date", validators = [DataRequired(message = "Evaluation Date is a required field.")])
    program = SelectField('Program', coerce=int, choices=[], validate_choice=False)
    organisation = SelectField('Organisation', coerce=int, choices=[], validate_choice=False)
    submit = SubmitField("Submit")

    def validate_amount(form,field):
        d = decimal.Decimal(field.data)
        n = abs(d.as_tuple().exponent)
        if (n>2):
            raise ValidationError("Amount must have up to 2 decimal digits")

class OrganisationForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
    abbr = StringField(label = "Abbreviation", validators = [DataRequired(message = "Abbreviation is a required field.")])
    postal_code = IntegerField(label = "Postal Code", validators = [DataRequired(message = "Postal Code is a required field.")])
    street = StringField(label = "Street", validators = [DataRequired(message = "Street is a required field.")])
    city = StringField(label = "City", validators = [DataRequired(message = "City is a required field.")])
    street_number = IntegerField(label= "Street Number", validators= [DataRequired(message = "Street Number is a required field.")])

    submit = SubmitField("Submit")

class ExecutiveForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
   
    submit = SubmitField("Submit")

class ResearcherForm(FlaskForm):
    first_name = StringField(label = "First Name", validators = [DataRequired(message = "First Name is a required field.")])
    last_name = StringField(label = "Last Name", validators = [DataRequired(message = "Last Name is a required field.")])
    birth_date = IntegerField(label = "Birth Date", validators = [DataRequired(message = "Birth Date is a required field.")])
    sex = StringField(label = "Sex", validators = [DataRequired(message = "Sex is a required field.")])
    start_date = DateField(label = "Start Date", default = date.today())
    organisation = SelectField(label = "Organisation", choices=[], validate_choice=False)
    
    submit = SubmitField("Submit")

class ProgramForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
    address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.")])

    submit = SubmitField("Submit")