from flask import Flask, render_template, request

from Machine import Machine

from challengelist import challenges

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9843yhfiujkhsd837y4rcu43jfhsdufdsfsfj92348r this is fake mate'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<int:challenge_number>")
def challenge_page(challenge_number):
    challenge = getChallengeTextFromNumber(challenge_number)

    m = Machine(length=10,height=8)

    return render_template("challenge.html", challenge = challenge, all_challenges = challenges, machine = m)

@app.route("/<int:challenge_number>", methods = ['POST'])
def submit(challenge_number):
    challenge = getChallengeTextFromNumber(challenge_number)

    #if request.method == 'POST':

    return render_template("challenge.html", challenge = challenge, all_challenges = challenges, submission=None)


def getChallengeTextFromNumber(number):
    for c in challenges:
        if c['id'] == number:
            return c
    return None

if __name__ == "__main__":
    app.run(debug=True)
