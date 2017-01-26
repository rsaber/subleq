import re
import json

class Machine():
    def __init__(self, length=10, height=8, maxcycles = 1000):
        self.memory = [0]*length*height
        self.maxCycles = maxcycles
        self.currentCycle = 0
        self.size = length*height;
        self.length = length
        self.height = height
        self.pc = 0
        self.instruction = {
            'a' : 0,
            'b' : 0,
            'c' : 0,
        }

    def reset(self):
        self.memory = [0]*self.size
        self.currentCycle = 0
        self.pc = 0
        self.instruction = {
            'a' : 0,
            'b' : 0,
            'c' : 0,
        }

    # Returns true if fetch successful ( not halt )
    # false otherwise
    def fetch(self):
        self.instruction['a'] = self.readMem(self.pc)
        self.instruction['b'] = self.readMem(self.pc+1)
        self.instruction['c'] = self.readMem(self.pc+2)
        if self.instruction['a'] == -1 and self.instruction['b'] == -1 and self.instruction['c'] == -1:
            raise ValueError("Halt")

    def execute(self):
        # subleq a, b, c   ; Mem[b] = Mem[b] - Mem[a]
        # if (Mem[b] <= 0) goto c
        self.currentCycle += 1
        if self.currentCycle > self.maxCycles:
            raise ValueError("Max cycles reached!")
        else:
            newB = self.readMem(self.instruction['b']) - self.readMem(self.instruction['a'])
            self.writeMem(newB,self.instruction['b'])
            if self.readMem(self.instruction['b']) <= 0:
                self.setPC(self.instruction['c'])
            else:
                self.setPC(self.pc + 3)

        self.pc = self.pc % self.size

    def run(self):
        while self.currentCycle <= self.maxCycles:
            self.fetch()
            self.execute()
            self.currentCycle += 1

    def readMem(self, index):
        if index > self.size - 1:
            raise ValueError("Address doesn't exist!")
        return self.memory[index]

    def readMemGrid(self, x,y):
        if y < self.height and x < self.length:
            return readMem((self.length*y)+x)
        else:
            raise ValueError("Address doesn't exist!")

    def readPC(self):
        return self.pc

    def setPC(self, new):
        if int(new) < self.size and int(new) >= 0:
            self.pc = new
        else:
            raise ValueError("Address doesn't Exist!")

    def readCurrentInstruction(self):
        return self.instruction

    def writeMem(self, value, index):
        if self.size < index or index < 0:
            raise ValueError("Address doesn't Exist!")
        self.memory[index] = value

    # returns the machine state as a json object
    def json(self, error):
        result = {}
        if error:
            result['error'] = error
        result['pc'] = self.pc
        result['len'] = self.length
        result['height'] = self.height
        for i,c in enumerate(self.memory):
            result[str(i)] = c
        return json.dumps(result)

    # Old way to import code, via text
    def loadInstructions(self, code, startPC = 0):
        self.pc = startPC
        for line in code:
            m = re.match(r'subleq\s(\d+)\s(\d+)\s(\d+)',line)
            if m is None:
                raise ValueError('Invalid Command')
            a = int(m.group(1))
            b = int(m.group(2))
            c = int(m.group(3))

            self.memory[self.pc] = a
            self.memory[self.pc+1] = b
            self.memory[self.pc+2] = c
            self.pc += 3

if __name__ == "__main__":
    # do tests here
    print("test")
