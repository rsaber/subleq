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
    machine.step()
    # return the encoded machine state
    return machine.json()

@app.route("/test/<int:challenge_number>", methods=['GET'])
def testCode(challenge_number):
    results = test(getChallengeTextFromNumber(challenge_number), request)
    return json.dumps({"output" : results[1]})

def getChallengeTextFromNumber(number):
    for c in challenges:
        if c['id'] == number:
            return c
    return None

# returns a tuple, element 0 is a boolean telling you if it passed all the tests ot not 
# element 1 is a array of output from the testing robot
def test(challenge, request):
    # decode the machine state
    machine = Machine(length=int(request.args['len']),height=int(request.args['height']))
    machine.pc = 0
    maxCell = int(request.args['len']) * int(request.args['height'])
    console = []
    # run the tests
    failed = False
    for test in challenge['tests']:
        # reset the machine
        machine.reset()
        for i in range(0,maxCell):
            machine.memory[i] = int(request.args[str(i)])
        # get the inputs and outputs
        inputs = test[0]
        outputs = test[1]
        # load the inputs
        for i in range(0,len(inputs)):
            machine.memory[inputs[i][1]] = inputs[i][0]
        # run the code
        machine.run()
        # check the outputs
        for i in range(0,len(outputs)):
            if machine.memory[outputs[i][1]] != outputs[i][0]:
                console.append("Test " + str(i) + " Failed : cell " + str(outputs[i][1]) + " should be " + str(outputs[i][0]) + " but is " + str(machine.memory[outputs[i][1]]))
                failed = True
    if failed == False:
            console.append("All tests passed, congrats!")
    return (failed, console)
if __name__ == "__main__":
    app.run(debug=True)
