from models import db, Learner, Coach, Lesson
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
        age=17,
        emergency_contact="07469656360",
        grade=0,
        email="demi@example.com"
    ),
]
    for learner in learners:
        learner.set_password("password123")
    db.session.add_all(learners)
    db.session.commit()
