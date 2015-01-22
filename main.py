import sys
import translator
import executor
import consolex

class EnhancedExecutor(executor.Executor, consolex.Consolex):
    
    def printRegs(self):
        print(' '.join([str(r) for r in self.regs]))
        print("acc=%d, cy=%d, ip=%d" % (self.acc, self.cy, self.ip))
    
    def c_3ff(self):
        self.printRegs()

def loadSource():
    if len(sys.argv) < 2:
        raise Exception('Source file should be specified!')
    fileName = sys.argv[1]
    f = open(fileName)
    lines = f.readlines()
    f.close()
    return lines

def fetchState(cpu):
    for i in range(2, len(sys.argv)):
        cpu.regs[i - 2] = int(sys.argv[i])

def main():
    try:
        src = loadSource()
        prg = translator.translate(src)
        cpu = EnhancedExecutor()
        fetchState(cpu)
        cpu.run(prg)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)

main()
