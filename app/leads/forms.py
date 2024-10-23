from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Optional

class LeadForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    contact_name = StringField('Contact Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    company_size = IntegerField('Company Size (Employees)', validators=[DataRequired()])
    industry = SelectField('Industry', choices=[
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('education', 'Education'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])