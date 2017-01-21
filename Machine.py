import re

class Machine():
    def __init__(self, size):
        self.memory = [0]*size
        self.size = size
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
        # if (Mem[b] ≤ 0) goto c

        if self.instruction['a'] < 0 or self.instruction['b'] < 0:
            self.pc -= 1
        else:
            self.memory[self.instruction['b']] -= self.memory[self.instruction['a']]

            if self.memory[self.instructuction['b'] <= 0]:
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

    def loadInstructions(self, code, startPC = 0):
        self.pc = startPC
        for line in code:
            m = re.match(r'subleq\s(\d+)\s(\d+)\s(\d+)',line)
            raise ValueError('Invalid Command') if m is None
            a = int(m.group(1))
            b = int(m.group(2))
            c = int(m.group(3))

            self.memory[self.pc] = a
            self.memory[self.pc+1] = b
            self.memory[self.pc+2] = c
            self.pc += 3

if __name__ == "__main__":
    # do tests here
