from datetime import date
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class ProjectForm(FlaskForm):
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])
    summary = TextAreaField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])
    start_date = DateField(label = "Start Date", default = date.today())
    end_date = DateField(label = "End Date", validators = [DataRequired(message = "End Date is a required field.")])
    amount = DecimalField(places = 2, label = "Amount", validators = [DataRequired(message = "Amount is a required field."), NumberRange(min = 100000, max = 1000000, message = "Amount must be between 100,000 and 1,000,000")])
    grade = DecimalField(places = 1, label= "Grade", validators= [DataRequired(message = "Amount is a required field."), NumberRange(min = 100000, max = 1000000, message = "Amount must be between 100,000 and 1,000,000")])
    evaluation_date = DateField(label= "Evaluation Date", validators = [DataRequired(message = "Evaluation Date is a required field.")])

    submit = SubmitField("Create")