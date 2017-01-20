import re

# How is subleq read in?
def subleqClean(codeInput):
 	code = re.sub(r'\n',' ',codeInput)
	code = re.sub(r'[^\d\s]','',code)
	code = re.sub(r'\s+',' ',code)
	code = re.sub(r'\s*$','',code)
	code = re.sub(r'^\s*','',code)
	code = code.split(" ")
	code = map(lambda x: int(x),code)
	return code

def subleqCompile(rawCode):
	code = subleqClean(rawCode)
	if len(code) % 3 != 0:
		raise NameError("Compilation Failed: incomplete subleq statement present")
	commandList = []
	for i in range(0,len(code)/3):
		index = i*3
		commandList.append((code[index],code[index+1],code[index+2]))
	result = []
	for command in commandList:
		result.append("ldi A "+str(command[0]))
		result.append("ldi B "+str(command[1]))
		# convert between line numbers and instructions
		result.append("ldi C "+str(10*(int(command[2])-1)))
		result.append("ld A A")          
		result.append("ld B B")
		result.append("ld C C")
		result.append("negi A ")          
		result.append("add B A ")
		result.append("ldi D 0 ")
		result.append("brle B D C")
	return "\n".join(result)

if __name__ == "__main__":
	code = "0 1 3\n 0 2 0\n 1 2 0"
	result = subleqCompile(code)
	print(result)