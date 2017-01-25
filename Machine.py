import re
import json

class Machine():
    def __init__(self, length, height):
        self.memory = [0]*length*height
        self.maxCycles = 1000 # defines at what point the machine decides it's in a infinite loop
        self.cycles = 0
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
        self.cycles = 0
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
            raise ValueError("HALT")

    def execute(self):
        # subleq a, b, c   ; Mem[b] = Mem[b] - Mem[a]
        # if (Mem[b] <= 0) goto c
        self.cycles += 1
        if self.cycles > self.maxCycles:
            raise ValueError("The Machine has exceeded the maximum number of allowed cycles. Possible Infinite Loop?")
        else:
            newB = self.readMem(self.instruction['b']) - self.readMem(self.instruction['a'])
            self.writeMem(newB,self.instruction['b'])
            if self.readMem(self.instruction['b']) <= 0:
                self.setPC(self.instruction['c'])
            else:
                self.setPC(self.readPC() + 3)

    def run(self):
        while self.pc <= self.size:
            self.fetch()
            self.execute()

    def readMem(self, index):
        if index > self.size - 1:
            raise ValueError("Index out of range")
        return self.memory[index]

    def readMemGrid(self, x,y):
        if y < self.height and x < self.length:
            return readMem((self.length*y)+x)
        else:
            raise ValueError('Index out of range')

    def readPC(self):
        return self.pc

    def setPC(self, new):
        if int(new) < self.size and int(new) >= 0:
            self.pc = new
        else:
            raise ValueError("Index out of range")
    def readCurrentInstruction(self):
        return self.instruction

    def writeMem(self, value, index):
        if self.size < index or index < 0:
            raise ValueError('Index out of range')
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
