import sys
import re
import copy
import languages.subleq

def match(text, regex):
	m = re.search("("+regex+")", text)
	if m:
		if m.group(1):
			return True
	return False
def tokenise(text):
	result = re.sub(r'\s+',r' ',text)
	result = re.sub(r'^\s*',r'',result)
	result = re.sub(r'\s*$',r'',result)
	return result.split(" ")


class MemorySegment():
	def __init__(self,name,size):
		self.name = name
		self.size = size
		self.data = [0]*size
	def write(self, address, data):
		if address >= 0 and address <= self.size-1:
			if type(data) == list:
				if address + len(data) > self.size-1:
					self.raiseError("Attempt to write to beyond memory bounds")
				c = 0
				for i in range(address,address+len(data)):
					self.data[i] = int(data[c])
					c = c + 1
			else:
				self.data[address] = int(data)
		else:
			self.raiseError("Attempt to access non-existant memory")
	def read(self, address):
		if address >= 0 and address <= self.size-1:
			return self.data[address]
		else:
			self.raiseError("Attempt to access non-existant memory")
	def raiseError(self, msg):
		message = "[Memory Segment: "+self.name+"] "+msg
		raise ValueError(message)

class VM():
	# Initalise the VM
	# size will set up a initial segment of memory
	# maxCycles defines at how many cycles the vm will stop running
	#    set this as 1000 or something to allow a large amount of 
	#    code to run but to stop any infinite loops
	def __init__(self, size, maxCycles):
		self.memorySegments = {}
		self.memorySegments['main'] = MemorySegment('main', size)
		self.memory = self.memorySegments['main']
		self.maxCycles = maxCycles
		self.size = size
		self.code = []
		self.pc = 0
		self.finished = False
		self.functions = {}
		self.inDefinition = None
		self.numRegisters = 8
		self.registers = {
			'R0' : 0,
			'R1' : 0,
			'R2' : 0,
			'R3' : 0,
			'R4' : 0,
			'R5' : 0,
			'R6' : 0,
			'R7' : 0
		}
		self.cycles = 0
		self.skipCurr = False
		self.debug = False
	# Load in some code
	def loadCode(self, code):
		codeArray = code.split('\n')
		for line in codeArray:
			if not line or match(line, r'^\s*$'):
				continue
			tokens = tokenise(line)
			strArray = "['"+"','".join(tokens[1:])+"']"
			self.code.append("self."+tokens[0]+"("+strArray+")")

	# Run the code that's been loaded in
	def run(self):
		if len(self.code) == 0:
			self.raiseError("Virtual Machine has no code loaded in to run")
		while self.finished == False:
			self.incCycles()
			if self.skipCurr == True:
				self.skipCurr = False
			elif self.code[self.pc] == "self.end([''])":
				eval(self.code[self.pc])
			elif self.inDefinition != None:
				self.functions[self.inDefinition].append(self.code[self.pc])
			else:
				eval(self.code[self.pc])
			self.pc = self.pc + 1
			if self.pc > len(self.code)-1:
				self.finished = True
	def jump(self, params):
		n = self.getVal(params[0])
		if self.pc+n > len(self.code)-1 or self.pc+n < 0:
			self.raiseError('Attempt to jump out of bounds')
		self.pc = self.pc + n
	def set(self, params):
		a = params[0]
		b = params[1]
		self.setVal(a, self.getVal(b))
	def sub(self, params):
		a = params[0]
		b = params[1]
		c = params[2]
		self.setVal(c, self.getVal(a) - self.getVal(b))
	def add(self, params):
		a = params[0]
		b = params[1]
		c = params[2]
		self.setVal(c, self.getVal(a) + self.getVal(b))
	def memLoad(self, params):
		address = params[0]
		self.setVal(address, params[1:])
	def cmp(self, params):
		a = self.getVal(params[0])
		b = params[1]
		c = self.getVal(params[2])
		sub = [params[3]]
		if b == '>' and a > c:
			self.runFunction(sub)
		elif b == '<=' and a <= c:
			self.runFunction(sub)
		elif b == '=' and a == c:
			self.runFunction(sub)

		if b != '=' and b != '<=' and b != '>':
			self.raiseError("Invalid comparator")
	def runFunction(self, params):
		sub = params[0]
		if sub not in self.functions:
			self.raiseError("Attempt to call non existant function")
		for line in self.functions[sub]:
			if self.skipCurr == True:
				self.skipCurr = False
				continue
			eval(line)
	def incCycles(self):
		self.cycles = self.cycles + 1
		if self.cycles > self.maxCycles:
			raise ValueError("Machine surpassed max cycles, possible infinite loop")
	def setVal(self, param, data):
		# reference
		if match(param, r'^\*\d+\:.*$'):
			param = re.sub(r'\*',r'',param)
			a = int(param.split(':')[0])
			n = param.split(':')[1]
			if n == "":
				memseg = self.memory
			else:
				if n not in self.memorySegments:
					self.raiseError("Attempt to access non-existant memory segment")
				memseg = self.memorySegments[n]
			address = memseg.read(a)
			memseg.write(address, data)

		# register reference
		elif match(param, r'\*[rR]\d:$'):
			try:
				num = param.split('r')[1]
				num = num.split(':')[0]
			except:
				num = param.split('R')[1]
				num = num.split(':')[0]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			reg = param.upper()
			reg = reg.split(":")[0]
			reg = reg.split("*")[1]
			address = self.memory.read(self.registers[reg])
			return self.memory.write(address, data)
		# register address
		elif match(param, r'^[rR]\d\:$'):
			try:
				num = param.split('r')[1]
				num = num.split(':')[0]
			except:
				num = param.split('R')[1]
				num = num.split(':')[0]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			reg = param.upper()
			reg = reg.split(":")[0]
			return self.memory.write(self.registers[reg], data)	
		# register
		elif match(param, r'^[rR]\d$') :
			try:
				num = param.split('r')[1]
			except:
				num = param.split('R')[1]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			self.registers[param.upper()] = data
		# address
		elif match(param, r'^\d+\:.*$'):
			a = int(param.split(':')[0])
			n = param.split(':')[1]
			if n == "":
				memseg = self.memory
			else:
				if n not in self.memorySegments:
					self.raiseError("Attempt to access non-existant memory segment")
				memseg = self.memorySegments[n]
			memseg.write(a, data)
		else:
			self.raiseError("Command refused input: " + param)
	def skip(self, params):
		data = self.getVal(params[0])
		if data != 0:
			self.skipCurr = True
	def newMemSeg(self, params):
		name = params[0]
		size = int(params[1])
		if name in self.memorySegments:
			self.raiseError("Memory segment label already in use")
		self.memorySegments[name] = MemorySegment(name, size)
	def setMemSeg(self, name):
		if name not in self.memorySegments:
			self.raiseError("Attempt to access non-existant memory segment")
		else:
			self.memory = self.memorySegments[name]
	def define(self, params):
		self.inDefinition = params[0]
		self.functions[params[0]] = []
	def end(self, params):
		self.inDefinition = None
	def memLoad(self, params):
		a = self.getVal(params[0])
		self.memory.write(a, params[1:])

	# Get the value of a paramter
	def getVal(self, param):
		# reference
		if match(param, r'^\*\d+\:.*$'):
			param = re.sub(r'\*',r'',param)
			a = int(param.split(':')[0])
			n = param.split(':')[1]
			if n == "":
				memseg = self.memory
			else:
				if n not in self.memorySegments:
					self.raiseError("Attempt to access non-existant memory segment")
				memseg = self.memorySegments[n]
			address = memseg.read(a)
			return memseg.read(address)
		# register reference
		elif match(param, r'\*[rR]\d:$'):
			try:
				num = param.split('r')[1]
				num = num.split(':')[0]
			except:
				num = param.split('R')[1]
				num = num.split(':')[0]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			reg = param.upper()
			reg = reg.split(":")[0]
			reg = reg.split("*")[1]
			address = self.memory.read(self.registers[reg])
			return self.memory.read(address)
		# register address
		elif match(param, r'^[rR]\d\:$'):
			try:
				num = param.split('r')[1]
				num = num.split(':')[0]
			except:
				num = param.split('R')[1]
				num = num.split(':')[0]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			reg = param.upper()
			reg = reg.split(":")[0]
			return self.memory.read(self.registers[reg])
		# register normal
		elif match(param, r'^[rR]\d$'):
			try:
				num = param.split('r')[1]
			except:
				num = param.split('R')[1]
			if int(num) > self.numRegisters-1:
				self.raiseError('Attempt to access non-existant register')
			return self.registers[param.upper()]
		# address
		elif match(param, r'^\d+\:.*$'):
			a = int(param.split(':')[0])
			n = param.split(':')[1]
			if n == "":
				memseg = self.memory
			else:
				if n not in self.memorySegments:
					self.raiseError("Attempt to access non-existant memory segment")
				memseg = self.memorySegments[n]
			return memseg.read(a)
		# immediate
		elif match(param, r'^\-?\d+$'):
			return int(param)
		else:
			self.raiseError("Command refused input: " + param)
	# only does main memory at the moment. 
	def memoryToHTML(self):
		memory = self.memory.data
		html = []
		html.append("<style>")
		html.append('.rwd-table {  margin: 1em 0;  min-width: 300px;}.rwd-table tr {  border-top: 1px solid #ddd;  border-bottom: 1px solid #ddd;}.rwd-table th {  display: none;}.rwd-table td {  display: block;}.rwd-table td:first-child {  padding-top: .5em;}.rwd-table td:last-child {  padding-bottom: .5em;}.rwd-table td:before {  content: attr(data-th) \'\';  font-weight: bold;  width: 6.5em;  display: inline-block;}@media (min-width: 480px) {  .rwd-table td:before {    display: none;  \}\}.rwd-table th, .rwd-table td {  text-align: left;}@media (min-width: 480px) {  .rwd-table th, .rwd-table td {    display: table-cell;    padding: .25em .5em;  }  .rwd-table th:first-child, .rwd-table td:first-child {    padding-left: 0;  }  .rwd-table th:last-child, .rwd-table td:last-child {    padding-right: 0;  \}\}.rwd-table {  background: rgba(52,73,94,0.6);  color: #fff;  border-radius: .4em;  overflow: hidden;}.rwd-table tr {  border-color: #46637f;}.rwd-table th, .rwd-table td {  margin: .5em 1em;}@media (min-width: 480px) {  .rwd-table th, .rwd-table td {    padding: 1em !important;  \}\}.rwd-table th, .rwd-table td:before {  color: #dd5;}')
		html.append("</style>")
		html.append("<table class='rwd-table' style='margin-bottom: 0px;'>")
		html.append("<tr><td><span style='color: #dd5'>0</span></td>")
		for i,cell in enumerate(memory):
			if i % 14 == 0 and i != 0:
				html.append("</tr><tr><td><span style='color: #dd5'>"+str(i)+"</span></td>")
			html.append("<td>" + str(cell) + "</td>")
		html.append("</tr>")
		html.append("</table>")
		return "".join(html)

	def raiseError(self, msg, **optional):
		line = self.code[self.pc].split('.')[1]
		line = re.sub(r'[\[\]\(\)\',]',r' ',line)
		line = re.sub(r'\s+',r' ',line)
		line = re.sub(r'\s*$',r'',line)
		message = msg + " ("+line+")"
		raise ValueError(message)

if __name__ == "__main__":
	machine = VM(1024, 1000)
	machine.loadCode('''
memLoad 0 3 4 6
memLoad 3 7 7 7
set r0 0
set r3 0
set r5 0
set r4 5
define leq
    set r0 r2:
    set r3 1
end
define quit
    set r5 1
end
add r0 1 r1
add r1 1 r2
sub *r1: *r0: *r1:
cmp *r1: <= 0 leq
skip r3
add r2 1 r0
set r3 0
cmp r0 > r4 quit
skip r5
jump -9
	''')
	machine.run()
	print(machine.memory.data)