from flask import Flask, request, jsonify, render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
db = SQLAlchemy(app)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Full_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Integer, unique=True)
    message= db.Column(db.String(50), nullable=False)
    students = db.relationship("Post", backref="teacher")  # uselist=False потрібен для One-to-One


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Full_name=db.Column(db.String(50), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))


@app.route("/")
def home():
    return render_template("hom.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method=="POST":
        student_name=request.form.get("name")
        if student_name in Students.query.filter_by(Full_name="").first_or_404():
            pass
        else:
            redirect("wrong.html")
        student= Students.query.filter_by(Full_name=student_name).first_or_404()
        teacher=student.teacher_id
        return teacher.message

@app.route("/admin")
def admin():
    return render_template("Admin_login.html")

@app.route("/login_admin", methods=["POST"])
def login_as_admin():
    if request.method=="POST":
        password=Teacher.query.filter_by(request.form.get("password")).all()
        if password:
           return redirect("messages.html")

@app.route("/left_message")
def left_messages():
    text=request.form.get("message")
    teacher=Teacher.query.filter_by(id=1).first()
    new_teacher=Teacher(Full_name="aaa",password="11111111",message=text)
    db.session.delete(teacher)
    db.session.add(new_teacher)
    db.session.commit()







if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)