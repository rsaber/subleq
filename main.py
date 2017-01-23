from flask import Flask, render_template, request
import json
import time
from Machine import Machine

from challengelist import challenges

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9843yhfiujkhsd837y4rcu43jfhsdufdsfsfj92348r this is fake mate'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<int:challenge_number>", methods=['GET'])
def challenge_page(challenge_number):
    challenge = getChallengeTextFromNumber(challenge_number)
    m = Machine(length=10,height=8) 
    # note that tag is just a unique number so that the broswer is forced to update files like css and js when we change them
    # rather then ignoring our changes and reading from cache
    return render_template("challenge.html", challenge = challenge, all_challenges = challenges, machine = m, tag = str(time.time()))

@app.route("/step", methods=['GET'])
def step():
    # decode the machine state
    machine = Machine(length=int(request.args['len']),height=int(request.args['height']))
    machine.pc = int(request.args['pc'])
    maxCell = int(request.args['len']) * int(request.args['height'])
    for i in range(0,maxCell):
        machine.memory[i] = int(request.args[str(i)])
    # step foward one bit of code
    machine.fetch()
    machine.execute()
    # return the encoded machine state
    return machine.json()



def getChallengeTextFromNumber(number):
    for c in challenges:
        if c['id'] == number:
            return c
    return None

if __name__ == "__main__":
    app.run(debug=True)
