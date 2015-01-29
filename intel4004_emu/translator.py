class Instruction(object):
    opcodes = {
        'nop': (1, 0),
        'jcn': (2, 2),
        'fim': (2, 2),
        'jun': (2, 1),
        'fin': (1, 1),
        'jms': (2, 1),
        'inc': (1, 1),
        'isz': (1, 2),
        'add': (1, 1),
        'sub': (1, 1),
        'ld': (1, 1),
        'xch': (1, 1),
        'bbl': (1, 1),
        'ldm': (1, 1),
        'clb': (1, 0),
        'clc': (1, 0),
        'iac': (1, 0),
        'cmc': (1, 0),
        'cma': (1, 0),
        'ral': (1, 0),
        'rar': (1, 0),
        'tcc': (1, 0),
        'dac': (1, 0),
        'stc': (1, 0),
        'daa': (1, 0),
        'tcs': (1, 0),

        'src': (1, 1),
        'wrm': (1, 0),
        'rdm': (1, 0),
        'adm': (1, 0),
        'sbm': (1, 0),
    }

class Line(object):
    
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
    
    def isCode(self):
        return self.parts[0] != 'db'
    
    def parseInstruction(self, addr):
        inTheLine = "in the line %d!" % self.index
        self.opcode = self.parts[0]
        self.params = self.parts[1:]
        try:
            size, params = Instruction.opcodes[self.opcode]
        except KeyError:
            raise Exception("Unknown instruction %s %s" % (self.opcode, inTheLine))
        if len(self.parts) != params + 1:
            raise Exception("Expected %d parameters %s" % (params, inTheLine))
        self.size = size
        self.addr = addr
    
    def parseData(self, addr):
        #this should be made to work with hex and strings later
        self.data = [int(x) for x in self.parts[1:]]
        self.size = len(self.data)
        self.addr = addr
    
    def __str__(self):
        return str(self.addr) + ": " + self.opcode + " " + ' '.join([str(x) for x in self.params])
    
    def __repr__(self):
        return '"' + self.__str__() + '"'

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
    linesRes = []
    labels = {}
    addr = 0
    for line in lines:
        label = line.stripLabel()
        if label != None:
            labels[label] = addr
            if len(line.text) == 0:
                continue
        line.splitParts()
        if line.isCode():
            line.parseInstruction(addr)
        else:
            line.parseData(addr)
        addr += line.size
        linesRes.append(line)
    return linesRes, labels


def secondPass(lines, labels):
    prg = {}
    for line in lines:
        if not line.isCode():
            for offset in range(len(line.data)):
                prg['d' + str(line.addr + offset)] = line.data[offset]
            continue
        cntParams = len(line.params)
        for j in range(cntParams):
            p = line.params[j]
            if p in labels:
                line.params[j] = labels[p]
            elif p[0] == 'r':
                line.params[j] = int(p[1:])
            elif p[0] == '$':
                line.params[j] = int(p[1:], 16)
            elif p.isdigit():
                line.params[j] = int(p)
        prg[line.addr] = line
    return prg

def translate(src):
    lines = prepareLines(src)
    lines, labels = firstPass(lines)
    prg = secondPass(lines, labels)
    return prg

