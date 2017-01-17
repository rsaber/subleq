import sys
import re

class VM():
	#initalise the VM
	def __init__(self, memSize):
		self.memSize = memSize
		self.memory = [0]*memSize
		self.pc = 0
		self.memPointer = 0
		self.formattedCode = ""
		self.finished = False
		self.code = []
	# Load code into memory and reset program counter
	def loadCode(self, codeInput):
		self.formattedCode = codeInput
		# Clean
		code = re.sub(r'\n',' ',codeInput)
		code = re.sub(r'[^\d\s]','',code)
		code = re.sub(r'\s+',' ',code)
		code = re.sub(r'\s*$','',code)
		code = re.sub(r'^\s*','',code)
		code = code.split(" ")
		self.code = map(lambda x: int(x),code)
		# reset program counter
		self.pc = 0
	# Set a certain memory cell
	def memSet(self, address, value):
		if address > self.memSize-1 or address < 0:
			raise NameError("Attempt to write to non-existant memory")
			return
		self.memory[address] = value
	# Get a memory value
	def memGet(self, address):
		if address > self.memSize-1 or address < 0:
			raise NameError("Attempt to read non-existant memory")
			return
		return self.memory[address]
	# Jump to a address
	def jump(self, address):
		if address > self.memSize-1 or address < 0:
			raise NameError("Attempt to jump to non-existant memory")
			return
		self.pc = address
	# Step foward 1 command
	def step(self):
		if self.pc+2 > self.memSize-1:
			self.finished = True
			return
		# Get addresses
		curr = self.pc
		A = self.code[curr]
		B = self.code[curr+1]
		C = self.code[curr+2]
		# sub: B = B-A
		self.memSet(B,self.memGet(B)-self.memGet(A))
		# leq
		if self.memGet(B) <= 0:
			# Move foward
			self.jump(C)
		else:
			# Try again
			self.pc = curr
	# Get a range of mem values
	def memGetRange(self, start, end):
		result = []
		if end < start:
			raise NameError("Attempt to read invalid range")
			return
		for address in range(start,end+1):
			result.append(self.memGet(address))
		return result
	# Prints out the memory to terminal
	def printMem(self, rowSize):
		if rowSize > self.memSize:
			raise NameError("rowSize exceeds memory size")
			return
		for i in range(0,self.memSize):
			if i % rowSize == 0:
				sys.stdout.write('\n')
				sys.stdout.write("{0:<3}  ".format(i))
			sys.stdout.write("{0:<3}".format(self.memGet(i)))
		sys.stdout.write('\n')

	# Runs the machine until it hits end of memory by default
	# Can be given the "for" paramters to specify a number of steps
	def run(**params):
		# Run for some amount of steps
		if "for" in params:
			steps = params["for"]
			if steps < 0 or steps > self.memSize:
				raise NameError("Invalid number of steps")
			for i in range(0,steps):
				if self.finished == True:
					break
				self.step()
		# Default
		else:
			while self.finished == False:
				self.step()


if __name__ == "__main__":
	machine = VM(9)
	machine.loadCode("0 2 3 2 1 6 0 0 0")
	machine.memSet(0,6)
	machine.memSet(1,4)
	machine.memSet(2,0)
	machine.printMem(3)
	machine.step()
	machine.printMem(3)
	machine.step()
	machine.printMem(3)

