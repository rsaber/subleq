from flask import Flask, render_template, request, g, session, redirect
import re
import VM
import languages.subleq
app = Flask(__name__)
app.secret_key = 'FUCK YOU SHOULD NOT BE SEEING THIS'

# Main page
@app.route('/', methods=['GET', 'POST'])
def BFD():
	# Set up initial machine state
	machine = VM.VM(84,100)
	machine.debug = True
	machine.memory.write(82,5)
	machine.memory.write(83,6)

	# On initial connection / reload
	if request.method == "GET":
		return render_template("index.html", memory=machine.memoryToHTML())
	# On reciving a request to run the code
	else:
		if "run" in request.form:
			# Check for no code
			rawCode = request.form["code"]
			if rawCode == "":
				return render_template("index.html", memory=machine.memoryToHTML())
			# Compile code and run
			code = languages.subleq.subleqCompile(rawCode)
			print(code)
			machine.loadCode(code)
			machine.run()
			return render_template("index.html", inputCode=rawCode, memory=machine.memoryToHTML())
		else:
			raise ValueError("unexpected request")

if __name__ == '__main__':
    app.run(debug=True)