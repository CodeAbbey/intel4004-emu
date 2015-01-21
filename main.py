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

def main():
    try:
        src = loadSource()
        prg = translator.translate(src)
        cpu = executor.Executor()
        cpu.run(prg)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)

main()
