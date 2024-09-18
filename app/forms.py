from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length

class DatabaseForm(FlaskForm):
    serial = IntegerField('Serial Number', render_kw={'readonly': True})
    UPC = StringField('UPC', validators=[
        DataRequired(),
        Length(min=12, max=12, message="UPC must be exactly 12 characters long")
    ])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    two_percent = BooleanField('2%')
    seven_percent = BooleanField('7%')
    submit = SubmitField('Generate')

    def validate_UPC(self, field):
        if not field.data.isdigit():
            raise ValidationError("UPC must contain only digits")