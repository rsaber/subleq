
def step(m):
	c = m.code[m.pc]
	#Movement commands
	if c == "<":
		m.memMove(-1)
	elif c == ">":
		m.memMove(1)
	elif c == "+":
		m.memAdjustCurr(1)
	elif c == "-":
		m.memAdjustCurr(-1)
	elif c == ".":
		try:
			m.machineRamStore('output') = m.machineRamGet('output').append(chr(m.memGetCurr()))
		except:
			m.machineRamStore('output') = [chr(m.memGetCurr())]
	elif c == ",":
		raise NameError("No Handling of input yet ...")
	elif c == "[":
		# we count skipped loops in loop depth
		m.machineRamStore('loopDepth') = m.machineRamGet('loopDepth')+1
		if m.memGetCurr() == 0:
			# jump to the end of this loop.
			self.skip = True
		else:
			self.stack.append(self.index+1)
	elif c == "]":
		if self.memory[self.pointer] == 0:
			#loop over, pop and move on
			self.loopDepth-=1
			self.stack.pop()
		else:
			#loop is not over, keep going
			self.index = self.stack[-1]-1

def clean(code):
	done = re.sub(r'[^\<\>\+\-\,\.\[\]]',r'',code)
	return done