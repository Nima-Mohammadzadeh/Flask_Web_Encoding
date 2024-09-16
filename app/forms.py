from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class DatabaseForm(FlaskForm):
    serial = IntegerField('Serial Number')
    UPC = IntegerField('UPC', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    two_percent = BooleanField('2%')
    seven_percent = BooleanField('7%')
    submit = SubmitField('Generate')