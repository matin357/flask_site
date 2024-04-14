from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///university.db"
db = SQLAlchemy(app)

teacher_student_association = db.Table(  # асоціативна таблиця для зв'язку викладачів та студентів
    "teacher_student",
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"))
)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    students = db.relationship("Student",
                               secondary=teacher_student_association,  # вказівка використовувати нашу таблицю
                               backref="teachers")


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")
    # return render_template("register.html")


@app.route("/register", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["hashedPassword"]
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return f"User {new_user.username} created successfully"


@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    username = request.form["username"]
    password = request.form["hashedPassword"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found"
    if user.password != password:
        print(user.password, "from form", password)
        return f"Incorrect password"

    name = request.form["name"]
    new_teacher = Teacher(name=name)
    db.session.add(new_teacher)
    db.session.commit()
    return f"Teacher {new_teacher.name} created successfully"


@app.route("/add_student", methods=["POST"])
def add_student():
    username = request.form["username"]
    password = request.form["hashedPassword"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found"
    if user.password != password:
        print(user.password, "from form", password)
        return f"Incorrect password"
    name = request.form["name"]
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return f"Student {new_student.name} created"


@app.route("/pair_teacher_student", methods=["POST"])  # post request always in json
def pair_teacher_student():
    teacher_id = request.form["teacher_id"]
    student_id = request.form["student_id"]
    teacher = Teacher.query.get(teacher_id)
    student = Student.query.get(student_id)
    teacher.students.append(student)
    db.session.commit()
    return f"Teacher {teacher.name} and {student.name} paired successfully"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
