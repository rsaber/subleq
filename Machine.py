import re
import json

class Machine():
    def __init__(self, length, height):
        self.memory = [0]*length*height
        
        self.size = length*height;
        self.length = length
        self.height = height

        self.pc = 0
        self.instruction = {
            'a' : 0,
            'b' : 0,
            'c' : 0,
        }

    def fetch(self):
        self.instruction['a'] = self.memory[self.pc]
        self.instruction['b'] = self.memory[self.pc+1]
        self.instruction['c'] = self.memory[self.pc+2]

    def execute(self):
        # subleq a, b, c   ; Mem[b] = Mem[b] - Mem[a]
        # if (Mem[b] <= 0) goto c

        if self.instruction['a'] < 0 or self.instruction['b'] < 0:
            self.pc -= 1
        else:
            self.memory[self.instruction['b']] -= self.memory[self.instruction['a']]

            if self.memory[self.instruction['b']] <= 0:
                self.pc = self.instruction['c']
            else:
                self.pc += 3

    def run(self):
        while self.pc <= self.size:
            self.execute()

    def readMem(self, index):
        return self.memory[index]

    def readMemGrid(self, x,y):
        # dodge as, pls fix
        return readMem(x * sqrt(self.size) + y)

    def readPC(self):
        return self.pc

    def readCurrentInstruction(self):
        return self.instruction

    def writeMem(self, value, index):
        if self.size < index or index < 0:
            return ValueError('Index out of range')
        self.memory[index] = value
    # returns the machine state as a json object
    def json(self):
        result = {}
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
