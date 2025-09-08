# Hatfield Junior Swimming School (HJSS) Management System

## Overview
The HJSS Management System is a web-based application for managing swimming lessons, bookings, and reviews for learners. The system provides tools for learners to view timetables, book lessons, attend sessions, submit reviews, and for administrators to manage users and generate reports.

The application is built using Flask, SQLAlchemy, and Bootstrap, with data stored in a SQLite database.

## Features

### Learner Features
- Register and log in with email and password.
- View timetable filtered by:
  - Day
  - Grade
  - Coach
- Book lessons:
  - Can book lessons at current grade or one level higher.
  - Limit of 4 learners per lesson.
- Attend lessons:
  - Attending a lesson one grade higher increases the learner’s grade.
- Cancel bookings before attending lessons.
- Submit reviews and ratings (1–5) after attending lessons.
- View personal bookings, status, and reviews.

### Admin Features
- View all learners and their booking history.
- Access detailed reports:
  - **Learner report:** booked, cancelled, attended lessons and reviews.
  - **Coach report:** average rating received.
- Add new learners manually via the system.

## Technology Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Frontend:** HTML, Jinja2, Bootstrap 5
- **Database:** SQLite
- **Authentication:** Flask sessions with hashed passwords
- **Deployment:** Local server (`flask run`) or any WSGI-compatible host

## Database Models

### Learner
- Fields: `id, name, age, gender, grade, email, password_hash, emergency_contact, role`
- Relationships: `bookings → Booking`

### Coach
- Fields: `id, name`
- Relationships: `lessons → Lesson`

### Lesson
- Fields: `id, day, time, grade, coach_id`
- Relationships: `bookings → Booking`

### Booking
- Fields: `id, learner_id, lesson_id, status (booked, cancelled, attended), review, rating`

## Installation
```bash
git clone https://github.com/yourusername/hjss-management.git
cd hjss-management
python -m venv venv
# Activate virtual environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
python populate_data.py
flask run
