import sys

class Instruction():
    opcodes = {
        'nop': (1, 0),
        'iac': (1, 0),
        'add': (1, 1),
        'fim': (2, 2),
        'jun': (2, 2)
    }

class Line():
    
    def __init__(self, index, text):
        self.index = index
        self.text = text.strip().lower()

    def stripComment(self):
        pos = self.text.find(';')
        if pos >= 0:
            self.text = self.text[:pos].strip()

    def stripLabel(self):
        pos = self.text.find(':')
        if pos < 0:
            return None
        label = self.text[:pos]
        self.text = self.text[pos + 1:].strip()
        return label

    def splitParts(self):
        self.parts = self.text.split()

    def parseInstruction(self):
        instr = self.parts[0]
        if instr not in Instruction.opcodes:
            raise Exception("Unknown instruction %s in the line %d!" % (instr, self.index))

def loadSource():
    if len(sys.argv) < 2:
        raise Exception('Source file should be specified!')
    fileName = sys.argv[1]
    f = open(fileName)
    lines = f.readlines()
    f.close()
    return lines

def prepareLines(src):
    lines = []
    count = len(src)
    for i in range(count):
        line = Line(i + 1, src[i])
        line.stripComment()
        if len(line.text) == 0:
            continue
        lines.append(line)
    return lines

def firstPass(lines):
    labels = {}
    addr = 0
    for line in lines:
        label = line.stripLabel()
        if label != None:
            labels[label] = addr
            if len(line.text) == 0:
                continue
        line.splitParts()
        line.parseInstruction()


def secondPass(prg):
    pass

def main():
    try:
        src = loadSource()
        lines = prepareLines(src)
        prog = firstPass(lines)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)

main()
