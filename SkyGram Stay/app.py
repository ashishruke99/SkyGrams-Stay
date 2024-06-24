from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from forms import VillaForm
from models import db, Villa, Photo
import sqlite3
import os

app = Flask(__name__)
app.config.from_object(Config)
  # Add this line
# Initialize the databases
def init_db():
    with app.app_context():
        # SQLAlchemy database for villas and photos
        db.init_app(app)
        db.create_all()

    # SQLite database for users and plans
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            dob TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            place_to_visit TEXT NOT NULL,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            adults INTEGER NOT NULL,
            children INTEGER NOT NULL,
            infants INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('our_destination'))

@app.route('/explore')
def explore():
    return render_template('explore.html', role='user')

@app.route('/our_destination')
def our_destination():
    return render_template('our_destination.html', role='user')

@app.route('/list_your_property', methods=['GET', 'POST'])
def list_your_property():
    form = VillaForm()
    if form.validate_on_submit():
        try:
            new_villa = Villa(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                location=form.location.data,
                property_type=form.property_type.data,
                rooms=form.rooms.data,
                heard_about=form.heard_about.data,
                description=form.description.data,
                link=form.link.data
            )
            db.session.add(new_villa)
            db.session.commit()

            # Save photos
            if form.photos.data:
                photo_file = form.photos.data
                filename = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], photo_file.filename)
                photo_file.save(filename)
                new_photo = Photo(filename=photo_file.filename, villa_id=new_villa.id)
                db.session.add(new_photo)
                db.session.commit()

            return redirect(url_for('list_your_property'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    villas = Villa.query.order_by(Villa.timestamp.desc()).all()
    return render_template('list_your_property.html', form=form, villas=villas, role='user')

@app.route('/delete_villa', methods=['POST'])
def delete_villa():
    if request.method == 'POST':
        villa_id = request.form.get('villa_id')
        villa = Villa.query.get(villa_id)
        if villa:
            try:
                db.session.delete(villa)
                db.session.commit()
                return jsonify(status='success', message='Villa deleted successfully')
            except Exception as e:
                db.session.rollback()
                return jsonify(status='error', message=str(e))
        else:
            return jsonify(status='error', message='Villa not found')

    return jsonify(status='error', message='Invalid request method')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html', role='user')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', role='user')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                session['first_name'] = user[1]
                session['last_name'] = user[2]
                session['role'] = user[7]  # Role is stored in the 8th column (index 7)
                if session['role'] == "user":
                    return redirect(url_for('our_destination'))
                elif session['role'] == "admin":
                    return redirect(url_for('admin_dashboard'))
            else:
                error = 'Invalid email or password.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect(url_for('our_destination'))

# app.py

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    search_key = request.form.get('search_key', '').strip() if request.method == 'POST' else ''
    
    query_user = "SELECT * FROM users WHERE role='user'"
    params_user = ()

    if search_key:
        query_user += " AND (first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ? OR dob LIKE ?)"
        params_user = tuple(['%' + search_key + '%'] * 5)

    query_guest = "SELECT * FROM plans"
    params_guest = ()

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute(query_user, params_user)
        customers = c.fetchall()

    with sqlite3.connect('info.db') as conn:
        c = conn.cursor()
        c.execute(query_guest, params_guest)
        guest_customers = c.fetchall()

    villas = Villa.query.all()  # Fetch villas from the database

    return render_template('admin_dashboard.html', customers=customers, search_key=search_key, guest_customers=guest_customers, villas=villas)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form.get('first_name').capitalize()
        last_name = request.form.get('last_name').capitalize()
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        if not (first_name.isalpha() and last_name.isalpha()):
            error = 'First and last names must contain only alphabetic characters.'
            return render_template('create_account.html', error=error)

        if len(phone) != 10 or not phone.isdigit():
            error = 'Phone number must be 10 digits.'
            return render_template('create_account.html', error=error)

        if password != re_password:
            error = 'Passwords do not match.'
            return render_template('create_account.html', error=error)

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            try:
                c.execute('''INSERT INTO users (first_name, last_name, email, phone, dob, password, role)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (first_name, last_name, email, phone, dob, password, "user"))
                conn.commit()
                success_message = f'{first_name} {last_name}, your account has been created successfully!'
                return render_template('create_account.html', success_message=success_message)
            except sqlite3.IntegrityError as e:
                if "email" in str(e):
                    error = 'Email already exists.'
                elif "phone" in str(e):
                    error = 'Phone number already exists.'
                else:
                    error = 'An error occurred. Please try again.'
                return render_template('create_account.html', error=error)

    return render_template('create_account.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            mobile = request.form['mobile']
            place = request.form['place']
            checkin = request.form['checkin']
            checkout = request.form['checkout']
            adults = int(request.form['guest_adults'])
            children = int(request.form['guest_children'])
            infants = int(request.form['guest_infants'])

            conn = sqlite3.connect('info.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO plans (name, email, mobile, place, checkin, checkout, adults, children, infants)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, mobile, place, checkin, checkout, adults, children, infants))
            conn.commit()
            conn.close()
            
            return jsonify(status='OK')
    except Exception as e:
        return jsonify(status='Error', message=str(e))

@app.route('/view')
def view():
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plans')
    plans = cursor.fetchall()
    conn.close()
    return render_template('view.html', plans=plans)

@app.route('/properties')
def view_properties():
    villas = Villa.query.all()
    if not villas:
        flash('No properties found.')
    else:
        for villa in villas:
            print(villa)  # Log the villas for debugging
    return render_template('properties.html', villas=villas)

@app.route('/property/<int:villa_id>')
def view_property(villa_id):
    villa = Villa.query.get_or_404(villa_id)
    return render_template('property_detail.html', villa=villa)

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(debug=True)
