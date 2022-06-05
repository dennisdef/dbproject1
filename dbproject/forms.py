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
    science_field1 = SelectField(label = "Science Field 1", choices = [('','')], validators = [DataRequired(message = "Science Field 1 is a required field.")])
    science_field2 = SelectField(label = "Science Field 2", choices = [('','')])
    executive = SelectField(label = "Executive", validators = [DataRequired(message = "Executive is a required field.")], choices = [])
    amount = DecimalField(places = 2, label = "Amount", validators = [DataRequired(message = "Amount is a required field."), NumberRange(min = 100000, max = 1000000, message = "Amount must be between 100,000 and 1,000,000")])
    grade = DecimalField(places = 1, label= "Grade", validators= [DataRequired(message = "Grade is a required field."), NumberRange(min = 0, max = 10, message = "Amount must be between 100,000 and 1,000,000")])
    evaluation_date = DateField(label= "Evaluation Date", validators = [DataRequired(message = "Evaluation Date is a required field.")])
    program = SelectField('Program', coerce=int, choices=[], validate_choice=False, validators = [DataRequired(message = "Program is a required field.")])
    organisation = SelectField('Organisation', coerce=int, choices=[], validate_choice=False, validators = [DataRequired(message = "Organisation is a required field.")])
    evaluator = SelectField('Evaluator', coerce=int, choices=[], validate_choice=False, validators = [DataRequired(message = "Evaluator is a required field.")])
    lead_researcher = SelectField('Lead Researcher', coerce=int, choices=[], validate_choice=False, validators = [DataRequired(message = "Lead Researcher is a required field.")])
    researchers = SelectMultipleField('Researchers', coerce=int, choices=[], validate_choice=False, validators = [DataRequired(message = "Researchers is a required field.")])
    submit = SubmitField("Submit")
            
    def validate_amount(form,field):
        d = decimal.Decimal(field.data)
        n = abs(d.as_tuple().exponent)
        if (n>2):
            raise ValidationError("Amount must have up to 2 decimal digits")

    def validate_grade(form,field):
        d = decimal.Decimal(field.data)
        n = abs(d.as_tuple().exponent)
        if (n>1):
            raise ValidationError("Amount must have up to 1 decimal digits")

    def validate_dates(form, self):
        if self.start_date.data > self.end_date.data:
            raise ValidationError("Start date must be before end date")
        if self.evaluation_date.data > self.start_date.data:
            raise ValidationError("Evaluation date must be before start date")
        if self.evaluation_date.data > self.end_date.data:
            raise ValidationError("Evaluation date must be before end date")
        if self.end_date.data - self.start_date.data < 365 or self.end_date.data - self.start_date.data > 365*4:
            raise ValidationError("Project must be between 1 and 4 years")


class OrganisationForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
    abbr = StringField(label = "Abbreviation", validators = [DataRequired(message = "Abbreviation is a required field.")])
    postal_code = IntegerField(label = "Postal Code", validators = [DataRequired(message = "Postal Code is a required field.")])
    street = StringField(label = "Street", validators = [DataRequired(message = "Street is a required field.")])
    city = StringField(label = "City", validators = [DataRequired(message = "City is a required field.")])
    street_number = IntegerField(label= "Street Number", validators= [DataRequired(message = "Street Number is a required field.")])
    phone = IntegerField(label = "Phone", validators = [DataRequired(message = "Phone is a required field.")])
    phone2 = IntegerField(label = "Phone 2", validators = [])
    phone3 = IntegerField(label = "Phone 3", validators = [])
    phone4 = IntegerField(label = "Phone 4", validators = [])
    phone5 = IntegerField(label = "Phone 5", validators = [])
    type = SelectField(label = "Organisation Type", choices=['-', 'Company', 'University', 'Research Center', ])
    equity = DecimalField(places = 2, label = "Equity", validators = [NumberRange(min = 100000, message = "Equity must be more than 100,000")])
    budget_pa = DecimalField(places = 2, label = "Budget", validators = [NumberRange(min = 100000, message = "Budget must be more than 100,000")])
    budget_me = DecimalField(places = 2, label = "Budget", validators = [NumberRange(min = 100000, message = "Budget must be more than 100,000")])
    
    submit = SubmitField("Submit")

    def validate_type(form, self):
        if self.type == "-":
            raise ValidationError("Select Organisation Type")

class ExecutiveForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
   
    submit = SubmitField("Submit")

class ResearcherForm(FlaskForm):
    first_name = StringField(label = "First Name", validators = [DataRequired(message = "First Name is a required field.")])
    last_name = StringField(label = "Last Name", validators = [DataRequired(message = "Last Name is a required field.")])
    birth_date = DateField(label = "Birth Date", validators = [DataRequired(message = "Birth Date is a required field.")])
    sex = StringField(label = "Sex", validators = [DataRequired(message = "Sex is a required field.")])
    start_date = DateField(label = "Start Date", default = date.today())
    organisation = SelectField(label = "Organisation", choices=[], validate_choice=False)

    submit = SubmitField("Submit")

class ProgramForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])
    address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.")])

    submit = SubmitField("Submit")


class SearchProjectForm(FlaskForm):
    start_date = DateField(label = "Start Date After:")
    end_date = DateField(label = "End Date Before:")
    length = SelectField(label = "Length", choices=[('0','-'), ('1','1'),('2','2'),('3','3'), ('4','4')])
    executive = SelectField(label = "Executive", choices=[])
    submit = SubmitField("Submit")

class DeliverableForm(FlaskForm):
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])
    summary = TextAreaField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])
    delivery_date = DateField(label = "Delivery Date", default = date.today())
    submit = SubmitField("Submit")