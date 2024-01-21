from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submit_form", methods=["POST"])
def submit_form():
    if request.method == "POST":
        return render_template("scam.html")


if __name__ == "__main__":
    app.run(debug=False)