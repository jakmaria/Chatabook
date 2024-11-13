from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from .models import db, User

# Define a blueprint for routes, keeping everything modular
bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_number= request.form.get('phone_number')
        password = request.form.get('password')
    
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email je už zaregistrovaný. Prosím prihláste sa.", 'warning')
            return redirect(url_for('main.login'))
    
        new_user = User(name=name, surname = surname, email = email, phone_number = phone_number, role_id = 4)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registrácia prebehla úspešne. Prosím prihláste sa.", 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Attempting login with email: {email}, password: {password}")

        user = User.query.filter_by(email=email).first()

        print(f"User found: {user is not None}")

        if user and user.check_password(password):
            print("Password is correct. Logging in user.")
            login_user(user)
            flash('Boli ste úspešne prihlásený!', 'success')
            return redirect(url_for('main.home'))
        else:
            print("Login failed: Incorrect email or password.")
            flash("Nesprávny prihlasovací email, alebo heslo!", 'danger')
    return render_template("login.html")

@bp.route('/logout')
def logout():
    logout_user()
    flash('Boli ste úspešne odhlásený!', 'info')
    return redirect(url_for('main.login'))