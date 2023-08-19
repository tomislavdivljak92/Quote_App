from flask import Flask ,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import psycopg2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://myfavquotes_user:xnEpJ3ewfqJ3kse5Ht4NXOQleYc44fvC@dpg-cjgcrbj6fquc73cpie90-a.frankfurt-postgres.render.com/myfavquotes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)


class Favquotes(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))

def fetch_and_store_quote():
    url = "https://dummyjson.com/quotes/random"
    response = requests.get(url)

    if response.status_code == 200:
        quote_data = response.json()
        quote_author = quote_data['author']
        quote_text = quote_data['quote']

        conn = psycopg2.connect(host="localhost", dbname="quotes", user="postgres", password="sifrazapostgre")
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO Favquotes(author, quote) VALUES (%s, %s)",
                (quote_author,quote_text)
            )
        conn.commit()
        conn.close()

@app.route("/")
def index():

    result = Favquotes.query.all()

    return render_template("index.html",result=result)

@app.route("/add_random_quote", methods=['GET','POST'])
def add_random_quote():
    if request.method == 'POST':
        fetch_and_store_quote()

    return redirect(url_for("index"))




@app.route("/quotes")
def quotes():
     return render_template("quotes.html")

@app.route("/process", methods=["POST"])
def process():


    author = request.form["author"]
    quote = request.form["quote"]
    quotedata = Favquotes(author=author,quote=quote)
    db.session.add(quotedata)
    db.session.commit()

    return redirect(url_for("index"))
