from flask import Flask, render_template, request
from Machine import Machine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9843yhfiujkhsd837y4rcu43jfhsdufdsfsfj92348r this is fake mate'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<int:challenge_number>")
def challenge():
    challenge = {
        'number' : challenge_number,
        'text' : getChallengeTextFromNumber(challenge_number)
    }
    return render_template("challenge.html", challenge)

def getChallengeTextFromNumber(number):
