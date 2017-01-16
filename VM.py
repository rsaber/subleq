import sys
import re

class VM():
	#initalise the VM
	def __init__(self, memSize):
		self.memSize = memSize
		self.memory = [0]*memSize
		self.pc = 0
		self.formattedCode = ""
	# Load code into memory and reset program counter
	def loadCode(self, codeInput):
		self.formattedCode = codeInput
		# Clean
		code = re.sub(r'\n',' ',codeInput)
		code = re.sub(r'[^\d\s]','',code)
		code = re.sub(r'\s+',' ',code)
		code = code.split(" ")
		# Move into memory
		for i,cell in enumerate(code):
			self.memSet(i,int(cell))
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
		# Get addresses
		curr = self.pc
		A = self.memGet(curr)
		B = self.memGet(curr+1)
		C = self.memGet(curr+2)
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
			sys.stdout.write("{0:<2}".format(self.memGet(i)))
		sys.stdout.write('\n')

if __name__ == "__main__":
	machine = VM(9)
	machine.loadCode("3 4 6 #This does some fun\n 7 7 7")
	machine.printMem(3)
	machine.step()
	machine.printMem(3)


