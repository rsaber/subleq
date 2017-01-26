from flask import Flask, render_template, request, redirect
import json
import time
from Machine import Machine
import copy
from challengelist import challenges

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9843yhfiujkhsd837y4rcu43jfhsdufdsfsfj92348r this is fake mate'


@app.route("/")
def index():
    return redirect("/1")

@app.route("/<int:challenge_number>", methods=['GET'])
def challenge_page(challenge_number):
    challenge = getChallengeTextFromNumber(challenge_number)
    if challenge is None:
        return redirect("/1")
    m = Machine()
    return render_template("challenge.html", challenge = challenge, all_challenges = challenges, machine = m, tag = str(time.time()))

@app.route("/step", methods=['GET'])
def step():
    # decode the machine state
    machine = Machine(length=int(request.args['len']),height=int(request.args['height']))
    machine.pc = int(request.args['pc'])
    maxCell = int(request.args['len']) * int(request.args['height'])
    for i in range(0,maxCell):
        machine.memory[i] = int(request.args[str(i)])

    # Keep a copy of this machine
    machineCopy = copy.deepcopy(machine)

    # Step foward one bit of code
    error = None
    try:
        machine.fetch()
        machine.execute()
    except ValueError as e:
        if str(e) != "HALT":
            error = str(e)
            # if an error occured revert the machine state back.
            machine = machineCopy

    # Return the encoded machine state
    return machine.json(error)

@app.route("/run", methods=['GET'])
def runCode():
    # decode the machine state
    machine = Machine(length=int(request.args['len']),height=int(request.args['height']))
    machine.pc = int(request.args['pc'])
    maxCell = int(request.args['len']) * int(request.args['height'])
    for i in range(0,maxCell):
        machine.memory[i] = int(request.args[str(i)])

    # Keep a copy of this machine
    machineCopy = copy.deepcopy(machine)
    # Run the code
    error = None
    try:
        machine.run()
    except ValueError as e:
        if str(e) != "HALT":
            error = str(e)
            # if an error occured revert the machine state back.
            machine = machineCopy
    # Return the encoded machine state
    return machine.json(error)

@app.route("/test/<int:challenge_number>", methods=['GET'])
def testCode(challenge_number):
    errors = None
    try:
        results = test(getChallengeTextFromNumber(challenge_number), request)
        return json.dumps({"output" : results[0]})
    except ValueError as e:
        return json.dumps({"error" : str(e)})

@app.route("/run", methods=['GET'])
def run(challenge_number):
    # decode the machine state
    machine = decodeMachineState(request)
    # Keep a copy of this machine
    machineCopy = copy.deepcopy(machine)
    # Run the code
    error = None
    try:
        machine.run()
    except ValueError as e:
        if str(e) != "HALT":
            error = str(e)
            #if error occured revert machine state
            machine = machineCopy
    # return the new state
    return machine.json(error)

# returns a machien based off a json input outlining the state
def decodeMachineState(request):
    machine = Machine(length=int(request.args['len']),height=int(request.args['height']))
    machine.pc = int(request.args['pc'])
    maxCell = int(request.args['len']) * int(request.args['height'])
    for i in range(0,maxCell):
        machine.memory[i] = int(request.args[str(i)])
    return machine

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
    passed = True
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
        try:
            machine.run()
        except ValueError as e:
            if str(e) != "HALT":
                raise e

        # check the outputs
        for i in range(0,len(outputs)):
            if machine.memory[outputs[i][1]] != outputs[i][0]:
                console.append("Test " + str(i) + " Failed : Cell " + str(outputs[i][1]) + " should be " + str(outputs[i][0]) + ", but is " + str(machine.memory[outputs[i][1]]))
                passed = False
    if passed == True:
            console.append("All tests passed!")
    return (passed, console)

if __name__ == "__main__":
    app.run(debug=True)
