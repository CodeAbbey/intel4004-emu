import sys
import translator
import executor

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
        cpu = executor.Executor()
        fetchState(cpu)
        cpu.run(prg)
        cpu.printRegs()
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)

main()
