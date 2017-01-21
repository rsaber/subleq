from flask import Flask, render_template, request, g, session, redirect
import re
import VM
import languages.subleq
app = Flask(__name__)
app.secret_key = 'FUCK YOU SHOULD NOT BE SEEING THIS'

# Main page
@app.route('/', methods=['GET', 'POST'])
def BFD():
	if request.method == "GET":
		return render_template("index.html")
	else:
		if "run" in request.form:
			rawCode = request.form["code"]
			code = languages.subleq.subleqCompile(rawCode)
			machine = VM.VM(16,1000)
			machine.loadCode(code)
			machine.run()
			return render_template("index.html", inputCode=rawCode, memory=memoryToHTML())
		elif "submit" in request.form:
			raise ValueError("unexpected request")
		else:
			raise ValueError("unexpected request")

# This needs to consider that the memory exists before the VM sets up (it has the input numbers in)
def memoryToHTML():
	return 0
if __name__ == '__main__':
    app.run(debug=True)