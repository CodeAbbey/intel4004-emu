#!/usr/local/bin/python2.7

import sys
import re
try:
    import translator
    import executor
except ImportError:
    from intel4004_emu import translator
    from intel4004_emu import executor

class EnhancedExecutor(executor.Executor):
    
    def __init__(self):
        super(EnhancedExecutor, self).__init__()
        self.inputCount = 0
        self.instructions = 0
    
    def step(self, line):
        super(EnhancedExecutor, self).step(line)
        self.instructions += 1
        if self.instructions > 1000000:
            raise Exception("Million instructions limit reached!")
    
    def printRegs(self):
        print(' '.join([("%x" % r) for r in self.regs]))

    def fetchState(self, data):
        data = data.strip()
        r = re.compile('^[0-9a-f](?:\s[0-9a-f]){15}$')
        if not r.match(data):
            return False
        data = data.split()
        for i in range(len(self.regs)):
            self.regs[i] = int(data[i], 16)
        return True

    def c_3f0(self):
        v = 0 if self.inputCount >= len(self.inputData) else ord(self.inputData[self.inputCount])
        self.inputCount += 1
        self.regs[3] = v & 0xF
        self.regs[2] = v >> 4
    
    def c_3e0(self):
        v = (self.regs[2] << 4) + self.regs[3]
        sys.stdout.write(chr(v))
    
def loadSource():
    text = sys.stdin.read().splitlines()
    if len(text) < 3:
        raise Exception('improper script invocation')
    inputCount = int(text[0].strip())
    return (text[inputCount + 1:], text[1 : inputCount + 1])

def main():
    print("Content-Type: text/plain")
    headerSent = False
    
    try:
        src, inputData = loadSource()
        prg = translator.translate(src)
        print("Program-Size: " + str(prg['_top']))
        print('')
        headerSent = True
        cpu = EnhancedExecutor()
        if len(inputData) == 1:
            if cpu.fetchState(inputData[0]):
                inputData = []
        cpu.inputData = '\n'.join(inputData)
        cpu.run(prg)
        if len(inputData) == 0:
            cpu.printRegs()
    except Exception as e:
        if not headerSent:
            print('')
        print("Error: %s\n" % e)

main()
