from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///documents.db"
db = SQLAlchemy(app)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namme = db.Column(db.String(50), nullable=False)
    kalories = db.Column(db.Integer, primary_key=False)
    Food_owner = db.relationship('Company', backref='comp', uselist=False)

class Company(db.Model):
    owner = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Integer, primary_key=False )
    name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)


@app.route("/", method="GET")
def home():
    name = request.args.get('name')
    company = Company.query.filter_by(reg_number=name).first()
    if company:
        food = company.food
        return jsonify({
            'name of food': food.namme,
            'kalories': food.kalories,
            'name of company': company.name,
            'owner of company': company.owner,
            'budget of company': company.reg_number,
        })
    else:
        return jsonify({'error': 'Food is not found'}), 404





def food_company():
    food = Food(namme="pop_korn",
                kalories=1024)
    db.session.add(food)
    owner = Company(owner="Rick_Astly",
                    budget=100000000000000,
                    name="Nestle")
    db.session.add(owner)
    db.session.commit()





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        food_company()
    app.run(debug=True)