from models import db, Learner, Coach, Lesson, Booking
from main import app

with app.app_context():
    db.create_all()
    c1 = Coach(name="Helen")
    c2 = Coach(name="Tom")
    c3 = Coach(name="Alice")
    db.session.add_all([c1, c2, c3])

    days = ["Monday", "Wednesday", "Friday", "Saturday"]
    times_week = {
        "Monday": ["4-5pm", "5-6pm", "6-7pm"],
        "Wednesday": ["4-5pm", "5-6pm", "6-7pm"],
        "Friday": ["4-5pm", "5-6pm", "6-7pm"],
        "Saturday": ["2-3pm", "3-4pm"],
    }

    lesson_id = 1
    for week in range(4):
        for day in days:
            for time in times_week[day]:
                for grade in range(1, 6):
                    lesson = Lesson(
                        day=day,
                        time=time,
                        grade=grade,
                        coach_id=(lesson_id % 3) + 1
                    )
                    db.session.add(lesson)
                    lesson_id += 1

    learners = [
    Learner(
        name="Emma",
        gender="Female",
        age=7,
        emergency_contact="077777777",
        grade=1,
        email="emma@example.com"
    ),
    Learner(
        name="Liam",
        gender="Male",
        age=8,
        emergency_contact="078888888",
        grade=2,
        email="liam@example.com"
    ),
    Learner(
        name="Noah",
        gender="Male",
        age=5,
        emergency_contact="07487906180",
        grade=0,
        email="noah@example.com"
    ),
    Learner(
        name="Demi",
        gender="Female",
        age=7,
        emergency_contact="07469656360",
        grade=0,
        email="demi@example.com"
    ),
    Learner(
        name="Sam",
        gender="Male",
        age=7,
        emergency_contact="07123456",
        grade=1,
        email="Sam@example.com"
    ),
    Learner(
        name="Koby",
        gender="Female",
        age=11,
        emergency_contact="0654321",
        grade=4,
        email="Koby@example.com"
    ),
    Learner(
        name="Ovi",
        gender="Male",
        age=4,
        emergency_contact="078967532343",
        grade=1,
        email="Ovi@example.com"
    ),
    Learner(
        name="Jack",
        gender="Male",
        age=6,
        emergency_contact="0779674532",
        grade=1,
        email="Jack@example.com"
    ),
    Learner(
        name="Cas",
        gender="Female",
        age=9,
        emergency_contact="077723132",
        grade=1,
        email="Cas@example.com"
    )
]
    for learner in learners:
        learner.set_password("password123")
    db.session.add_all(learners)
    admin = Learner(
    name="Admin",
    gender="M",
    age=30,
    emergency_contact="000000000",
    grade=0,
    email="admin@hjss.com",
    role="admin"
)
    all_lessons = Lesson.query.all()
    bookings = []
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    for i, learner in enumerate(learners):
        lesson = all_lessons[i % len(all_lessons)]
        booking = Booking(
            learner_id=learner.id,
            lesson_id=lesson.id,
            status='attended',
            review=f"Had a great time.",
            rating=(i % 5) + 1  
        )
        bookings.append(booking)
    
    db.session.add_all(bookings)
    db.session.commit()
