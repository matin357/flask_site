from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///documents.db"
db = SQLAlchemy(app)

Company_food = db.Table(
    "Companys_food",
    db.Column("company_id", db.Integer, db.ForeignKey("company.id")),
    db.Column("food_id", db.Integer, db.ForeignKey("food.id"))
)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    Food_made = db.relationship('Food',
                                secondary=Company_food,
                                backref='companys')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/add_company", methods=["POST"])
def add_company():
    name = request.form["name"]
    new_company = Company(name=name)
    db.session.add(new_company)
    db.session.commit()
    return f"Teacher {new_company.name} created successfully"


@app.route("/add_food", methods=["POST"])
def add_food():
    name = request.form["name"]
    new_food = Food(name=name)
    db.session.add(new_food)
    db.session.commit()
    return f"Student {new_food.name} created"


@app.route("/pair_company_food", methods=["POST"])  # post request always in json
def pair_company_food():
    company_id = request.form["teacher_id"]
    food_id = request.form["food_id"]
    company = Company.query.get(company_id)
    food = Food.query.get(food_id)
    company.students.append(food)
    db.session.commit()
    return f"Teacher {company.name} and {food.name} paired successfully"




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)