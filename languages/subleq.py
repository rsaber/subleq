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
		raise NameError("Compilation Failed, Incomplete subleq statement present")
	commandList = []
	for i in range(0,len(code)/3):
		index = i*3
		commandList.append((code[index],code[index+1],code[index+2]))
	result = []
	# copy code into memory
	curr = 0
	for command in commandList:
		temp = [str(command[0]),str(command[1]),str(command[2])]
		line = 'memload '+str(curr)+" "+" ".join(temp)
		curr+=3
		result.append(line)
	# write interaction code
	# A = 0
	result.append('set r0 0')
	result.append('set r3 0')
	result.append('define leq')
	result.append('    set r0 r2:')
	result.append('    set r3 1')
	result.append('end')
	for command in commandList:
		# B = A + 1
		result.append('add r0 1 r1')
		# C = B + 1
		result.append('add r1 1 r2')
		result.append('sub r1: r0: r1:')
		result.append('cmp r1: <= 0 leq')
		result.append('skip r3')
		result.append('add r2 1 r0')
		result.append('set r3 0')

	return "\n".join(result)

if __name__ == "__main__":
	code = "0 1 3\n 0 2 0\n 1 2 0"
	result = subleqCompile(code)
	print(result)