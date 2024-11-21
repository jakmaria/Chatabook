# Chatabook - Family Cottage Reservation System

#### Video Demo:

#### Description:
**Chatabook** is a web-based reservation system designed to simplify the management of a shared family cottage.

Chatabook is not just a booking platform—it’s a solution to the common challenges of managing shared family resources. With its intuitive design, it reduces the confusion and overlap in scheduling, ensuring every family member can plan their stay with confidence. By implementing role-based access, the system maintains fairness, allowing admins to oversee all bookings while giving regular users the ability to manage their own events.

The platform caters to various scenarios, from short family getaways to full-week cottage reservations. Guests can view availability without interfering, and admins can step in to manage user accounts or create bookings for others. This ensures seamless coordination and maximizes the utility of the family cottage.

## Technology Stack
Chatabook leverages modern web development technologies:

**Flask:** A lightweight Python framework ideal for scalable web applications.
**SQLAlchemy:** For robust database management and ORM functionality.
**FullCalendar.js:** Provides a dynamic and interactive calendar for viewing bookings.
**Flatpickr.js:** Enables user-friendly date selection.
**Bcrypt:** Ensures secure password hashing, safeguarding user credentials.
**Flask-Login:** Streamlines session management and user authentication.


---

## Features

1. **User Roles and Permissions:**
   - **Admin:** Full access to manage users and bookings.
   - **User:** Can create, edit, and delete their own bookings.
   - **Guest:** Read-only access to view bookings.
   - **Visitor:** Can log in but has minimal access for future expansion.

2. **Booking Management:**
   - Create new bookings with start and end dates.
   - View upcoming bookings in a sortable table and on an interactive calendar.
   - Option for the admin to create bookings on behalf of other users.
   - Users can create the events with choosing the dates, the type of the event and can also leave a comment.

3. **Interactive Calendar:**
   - Displays all bookings with distinct colors for full-cottage and partial-cottage reservations.
   - Calendar navigation for viewing bookings by month, week, or day.

4. **User Management:**
   - Admins can view, edit, or delete user accounts.

5. **Validation and Security:**
   - End date has to be later than the start date.
   - Password hashing for secure user authentication.

6. **Optional Features (Planned):**
   - Email notifications for booking confirmations and reminders.
   - Search and filter functionality for bookings.
   - Data validation
   - Forgotten password

---

### Files and Their Purpose

1. **app.py**
   - The main entry point for the application. Initializes the Flask app and runs the server.

2. **app/\_\_init\_\_.py**
   - Configures the Flask application and initializes extensions like SQLAlchemy, Bcrypt, and Flask-Login.

3. **app/models.py**
   - Defines the database models: `User`, `Booking`, `Role`, and `EventType`.
   - Establishes relationships and cascade behavior between users and their bookings.

4. **app/routes.py**
   - Contains the routes for the application, including home, booking, user management, login, and logout.

5. **app/templates/**
   - **layout.html:** The base template with a shared structure for all pages.
   - **index.html:** Displays the calendar, upcoming bookings, and a filter/search interface.
   - **login.html:** The login page for users.
   - **register.html:** The registration page for new users.
   - **booking.html:** The form for creating a new booking.
   - **edit_booking.html:** The form for editing an existing booking.
   - **manage_users.html:** Allows admins to view, edit, and delete users.
   - **403.html** After the user tries to access an unauthorizes route, he/she is redircted to this error page
   - **landing_page.html** ABout to be a page that a user lands on when not logged in.

6. **app/static/**
   - **styles.css:** Contains custom styles for the application.
   - **FullCalendar and Flatpickr integration files:** Ensure a responsive and interactive interface.

---

## Design and Implementation

### Frontend:
- Designed with Flask's templating engine and a focus on responsive design for usability.
- Utilizes FullCalendar.js for calendar functionality and Flatpickr.js for date selection.

### Backend:
- Built with Flask, leveraging its modular blueprint system for route management.
- Database management using SQLAlchemy ORM with SQLite.
- Implements Flask-Login for user authentication and role-based access control.

---

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd Chatabook
2. **Set Up a Virtual Environment:**
    ```
    python3 -m venv venv
    source venv/bin/activate 
   ``` 
    
3. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Initialize the Database:**
    ```
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
5. **Run the Application:**
    ```
    flask run
    ```
6. **Access the App:**
    Open your browser and navigate to
    ```http://127.0.0.1:5000 ```