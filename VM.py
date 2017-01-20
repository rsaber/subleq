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
		if address >= 0 and address < self.size-1:
			self.data[address] = data
		else:
			self.raiseError("Attempt to access non-existant memory")
	def read(self, address):
		if address >= 0 and address < self.size-1:
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
			if self.code[self.pc] == "self.end([''])":
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

		if b != '=' and b != '<' and b != '>':
			self.raiseError("Invalid comparator")
	def runFunction(self, params):
		sub = params[0]
		if sub not in self.functions:
			self.raiseError("Attempt to call non existant function")
		for line in self.functions[sub]:
			eval(line)
	def incCycles():
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
		# register
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
	''')
	machine.run()
	print(machine.registers)
