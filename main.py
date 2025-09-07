from flask import Flask, render_template, request, redirect, url_for
from models import db, Learner, Coach, Lesson, Booking
from flask import session



app = Flask(__name__)
app.secret_key = '123456789'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/learners', methods=['GET', 'POST'])
def learners():
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    

    learners = Learner.query.all()
    return render_template('learner.html', learners=learners)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        learner = Learner.query.filter_by(email=email).first()
        if learner and learner.check_password(password):
            session['learner_id'] = learner.id
            return redirect(url_for('timetable'))
        return "Invalid credentials."
    return render_template('login.html')
@app.route('/cancel/<int:booking_id>')
def cancel_booking(booking_id):
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(booking_id)

    if booking.learner_id != learner_id:
        return "You are not allowed to cancel this booking."

    if booking.status == "attended":
        return "You cannot cancel an attended lesson."

    booking.status = "cancelled"
    db.session.commit()
    return redirect(url_for('learners'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        grade = int(request.form['grade'])
        emergency_contact = request.form['emergency_contact']
        email = request.form['email']
        password = request.form['password']

        existing = Learner.query.filter_by(email=email).first()
        if existing:
            return "Email already registered."

        new_learner = Learner(
            name=name,
            age=age,
            gender=gender,
            grade=grade,
            emergency_contact=emergency_contact,
            email=email
        )
        new_learner.set_password(password)

        db.session.add(new_learner)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('learner_id', None)
    return redirect(url_for('login'))
@app.route('/timetable')
def timetable():
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    day = request.args.get('day')
    grade = request.args.get('grade')
    coach = request.args.get('coach')

    lessons = Lesson.query

    if day:
        lessons = lessons.filter_by(day=day)
    if grade:
        lessons = lessons.filter_by(grade=int(grade))
    if coach:
        coach_obj = Coach.query.filter_by(name=coach).first()
        if coach_obj:
            lessons = lessons.filter_by(coach_id=coach_obj.id)

    lessons = lessons.all()

    return render_template('timetable.html', lessons=lessons, learner_id=1)



@app.route('/book/<int:learner_id>/<int:lesson_id>')
def book_lesson(learner_id, lesson_id):
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    learner = Learner.query.get_or_404(learner_id)
    lesson = Lesson.query.get_or_404(lesson_id)

    if len(lesson.bookings) >= 4:
        return render_template("fulllesson.html")

    if lesson.grade > learner.grade + 1:
        return render_template("unsuccesfull1.html")

    existing = Booking.query.filter_by(learner_id=learner.id, lesson_id=lesson.id).first()
    if existing:
        return render_template("unsuccesfull2.html")

    booking = Booking(learner_id=learner.id, lesson_id=lesson.id, status='booked')
    db.session.add(booking)
    db.session.commit()

    return render_template("LessonBooked.html")
@app.route('/debug')
def debug():
    lessons = Lesson.query.all()
    return {
        "lesson_count": len(lessons),
        "lesson_ids": [lesson.id for lesson in lessons],
        "bookings_per_lesson": [len(lesson.bookings) for lesson in lessons]
    }

@app.route('/attend/<int:booking_id>')
def attend_lesson(booking_id):
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    booking = Booking.query.get(booking_id)
    booking.status = "attended"

    learner = booking.learner
    lesson = booking.lesson
    if lesson.grade == learner.grade + 1:
        learner.grade += 1

    db.session.commit()
    return redirect(url_for('learners'))

@app.route('/review/<int:booking_id>', methods=['GET', 'POST'])
def review(booking_id):
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    booking = Booking.query.get(booking_id)
    if request.method == 'POST':
        booking.review = request.form['review']
        booking.rating = int(request.form['rating'])
        db.session.commit()
        return redirect(url_for('learners'))
    return render_template('review.html', booking=booking)

@app.route('/reports/learners')
def report_learners():
    learner_id = session.get('learner_id')
    if not learner_id:
        return redirect(url_for('login'))
    learners = Learner.query.all()
    return render_template('learner_report.html', learners=learners)


@app.route('/reports/coaches')
def report_coaches():
    coaches = Coach.query.all()
    return render_template('coach_report.html', coaches=coaches)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
