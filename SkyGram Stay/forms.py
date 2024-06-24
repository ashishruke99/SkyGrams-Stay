from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp
from wtforms.validators import Optional, URL

class VillaForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone*', validators=[DataRequired(), Length(min=10, max=10), Regexp(r'^[0-9]*$', message="Phone number must be digits only")])
    location = SelectField('Location', choices=[('Kamshet', 'Kamshet'), ('Panshet', 'Panshet'), ('Lonavala', 'Lonavala'), ('Igatpuri', 'Igatpuri'), ('Karjat', 'Karjat'), ('Panchgani', 'Panchgani'), ('Mahableshwar', 'Mahableshwar'), ('Bhor', 'Bhor'), ('Alibaug', 'Alibaug'), ('Pawana', 'Pawana'), ('Dapoli', 'Dapoli'), ('Wai', 'Wai'), ('Mulshi', 'Mulshi'), ('Kashid', 'Kashid'), ('Khopoli', 'Khopoli'), ('Malavli', 'Malavli'), ('Khandala', 'Khandala')])
    property_type = SelectField('Property Type', choices=[('apartment', 'Apartment'), ('villa', 'Villa'), ('house', 'House')])
    rooms = StringField('Number of Rooms', validators=[Regexp(r'^[0-9]+$', message="Number of rooms must be a valid number")])
    heard_about = SelectField('How did you hear about us?', choices=[('insta', 'Instagram'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('blog', 'Blog'), ('customer', 'Customer'), ('villa_owner', 'Villa Owner'), ('website', 'Website')])
    photos = FileField('Photos')
    description = TextAreaField('Description')
    link = StringField('Link (optional)', validators=[Optional()], render_kw={"placeholder": "Enter link here"})
    submit = SubmitField('Send a request')

class VillaForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone*', validators=[DataRequired(), Length(min=10, max=10), Regexp(r'^[0-9]*$', message="Phone number must be digits only")])
    
    location = SelectField('Location', choices=[
        ('Kamshet', 'Kamshet'), ('Panshet', 'Panshet'), ('Lonavala', 'Lonavala'), ('Igatpuri', 'Igatpuri'),
        ('Karjat', 'Karjat'), ('Panchgani', 'Panchgani'), ('Mahableshwar', 'Mahableshwar'), ('Bhor', 'Bhor'),
        ('Alibaug', 'Alibaug'), ('Pawana', 'Pawana'), ('Dapoli', 'Dapoli'), ('Wai', 'Wai'), 
        ('Mulshi', 'Mulshi'), ('Kashid', 'Kashid'), ('Khopoli', 'Khopoli'), ('Malavli', 'Malavli'), ('Khandala', 'Khandala')
    ])
    
    property_type = SelectField('Property Type', choices=[('apartment', 'Apartment'), ('villa', 'Villa'), ('house', 'House')])
    rooms = StringField('Number of Rooms', validators=[Regexp(r'^[0-9]+$', message="Number of rooms must be a valid number")])
    heard_about = SelectField('How did you hear about us?', choices=[
        ('insta', 'Instagram'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('blog', 'Blog'), 
        ('customer', 'Customer'), ('villa_owner', 'Villa Owner'), ('website', 'Website')
    ])
    
    photos = FileField('Photos')
    link = StringField('Link (optional)', validators=[Optional()], render_kw={"placeholder": "Enter link here"})
    description = TextAreaField('Description')
    submit = SubmitField('Send a request')
