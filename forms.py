from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional

class VillaForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone*', validators=[DataRequired(), Length(min=10, max=10), Regexp(r'^[0-9]*$', message="Phone number must be digits only")])
    
    location = SelectField('Location', choices=[('', 'Select Location')])
    property_type = SelectField('Property Type', choices=[('', 'Select Property Type')])
    rooms = StringField('Number of Rooms', validators=[Regexp(r'^[0-9]+$', message="Number of rooms must be a valid number")], default='2')
    heard_about = SelectField('How did you hear about us?', choices=[('', 'Select an Option')])
    
    photos = FileField('Photos')
    link = StringField('Link (optional)', validators=[Optional()], render_kw={"placeholder": "Enter link here"})
    description = TextAreaField('Description')
    submit = SubmitField('Send a request')
    
    def __init__(self, *args, **kwargs):
        super(VillaForm, self).__init__(*args, **kwargs)
        self.location.choices += [
            ('Kamshet', 'Kamshet'), ('Panshet', 'Panshet'), ('Lonavala', 'Lonavala'), ('Igatpuri', 'Igatpuri'),
            ('Karjat', 'Karjat'), ('Panchgani', 'Panchgani'), ('Mahableshwar', 'Mahableshwar'), ('Bhor', 'Bhor'),
            ('Alibaug', 'Alibaug'), ('Pawana', 'Pawana'), ('Dapoli', 'Dapoli'), ('Wai', 'Wai'), 
            ('Mulshi', 'Mulshi'), ('Kashid', 'Kashid'), ('Khopoli', 'Khopoli'), ('Malavli', 'Malavli'), ('Khandala', 'Khandala')
        ]
        self.property_type.choices += [
            ('apartment', 'Apartment'), ('villa', 'Villa'), ('house', 'House')
        ]
        self.heard_about.choices += [
            ('insta', 'Instagram'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('blog', 'Blog'), 
            ('customer', 'Customer'), ('villa_owner', 'Villa Owner'), ('website', 'Website')
        ]
