from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from app.utils import role_required
from .models import db, User, Booking, EventType, Role
from datetime import datetime, date, timedelta
import json

# Define a blueprint for routes, keeping everything modular
bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template('landing_page.html')
    
    #Calendar display was implemented with the help of ChatGPT
    today = date.today() 
    bookings = Booking.query.filter(Booking.date_to >= today).order_by(Booking.date_from).all()
    events = [
        {
            "title": f"{booking.event_type.name} ({booking.user.name})",
            "start": booking.date_from.strftime("%Y-%m-%d"),
            "end": (booking.date_to + timedelta(days=1)).strftime("%Y-%m-%d"),  # FullCalendar excludes the end date
            "color": "#FFD700" if booking.whole_cottage else "#87CEEB"  # Optional: Color coding
        }
        for booking in bookings
    ]
    return render_template('index.html', bookings=bookings, events=events)

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

@bp.route('/booking', methods=['GET', 'POST'])
@role_required(2)
@login_required
def booking():

    from .models import Role

    users = None
    if current_user.role_id == 1:  # Admin
        users = User.query.all() 

    if request.method == 'POST':
        if current_user.role_id == 1:  
            user_id = request.form.get('user_id', current_user.id)
        else:  # Regular users
            user_id = current_user.id

        date_from = datetime.strptime(request.form.get('date_from'), "%Y-%m-%d").date()
        date_to = datetime.strptime(request.form.get('date_to'), "%Y-%m-%d").date()

        event_type_id = request.form.get('event_type_id', 1)
        whole_cottage = request.form.get('whole_cottage', True) 
        comment = request.form.get('comment')

        event_types = EventType.query.all()
        
        booking = Booking(
            user_id = user_id, 
            date_from = date_from,
            date_to = date_to,
            event_type_id = event_type_id,
            whole_cottage = whole_cottage,
            comment = comment
        )
        db.session.add(booking)
        db.session.commit()

        flash('Rezervácia bola úspešne vytvorená!', 'success')
        return redirect(url_for('main.home'))
    event_types = EventType.query.all()
    return render_template('booking.html',event_types=event_types, users=users)


@bp.route('/manage-users', methods=['GET'])
@role_required(1)  
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@bp.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
@role_required(2)  
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id and current_user.role_id > 1:
        abort(403)  # Forbidden

    event_types = EventType.query.all()

    if request.method == 'POST':

        booking.date_from = datetime.strptime(request.form.get('date_from'), "%Y-%m-%d").date()
        booking.date_to = datetime.strptime(request.form.get('date_to'), "%Y-%m-%d").date()
        booking.comment = request.form.get('comment')

        db.session.commit()
        flash("Rezervácia bola úspešne upravená!", "success")
        return redirect(url_for('main.home'))

    return render_template('edit_booking.html', booking=booking,event_types=event_types)

@bp.route('/delete-booking/<int:booking_id>', methods=['POST'])
@role_required(2)  
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id and current_user.role_id > 1:
        abort(403)  # Forbidden

    db.session.delete(booking)
    db.session.commit()
    flash("Rezervácia bola úspešne zmazaná!", "success")
    return redirect(url_for('main.home'))

@bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@role_required(1)  
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all() 

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.email = request.form.get('email')
        user.phone_number = request.form.get('phone_number')
        user.role_id = request.form.get('role_id')  

        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('main.manage_users'))

    return render_template('edit_user.html', user=user, roles=roles)

@bp.route('/delete-user/<int:user_id>', methods=['POST'])
@role_required(1)  
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for('main.manage_users'))

