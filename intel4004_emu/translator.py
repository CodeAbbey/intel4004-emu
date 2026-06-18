class Instruction(object):
    opcodes = {
        'nop': (1, 0),
        'jcn': (2, 2),
        'fim': (2, 2),
        'jun': (2, 1),
        'fin': (1, 1),
        'jms': (2, 1),
        'inc': (1, 1),
        'isz': (2, 2),
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
        self.text = text.strip()
        self.codeTop = 0
        self.dataTop = 0

    def stripLabel(self):
        pos = self.text.find(':')
        if pos < 0:
            return None
        label = self.text[:pos]
        for c in label:
            if not c.isalpha() and not c.isdigit() and c != '_':
                return None
        self.text = self.text[pos + 1:].strip()
        return label

    def splitParts(self):
        self.parts = []
        s = self.text + ' '
        n = len(s)
        p1 = 0
        while p1 < n:
            if s[p1].isspace():
                p1 += 1
                continue
            if s[p1] == ';':
                break
            if s[p1] == '\'':
                p2 = s.find('\'', p1 + 1)
                if p2 < 0:
                    raise "Unmatched quote in the line %" % self.index
                self.parts.append(s[p1 + 1 : p2])
                p1 = p2 + 1
            else:
                p2 = p1
                while not s[p2].isspace():
                    p2 += 1
                v = s[p1:p2].lower()
                if v.isdigit():
                    v = int(v)
                elif v[0] == '$':
                    v = int(v[1:], 16)
                self.parts.append(v)
                p1 = p2
    
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
        if self.opcode=='ld' and not (type(self.params[0]) is str) :
            raise Exception("Expected register parameter for ld instruction  %s" % ( inTheLine))
        self.size = size
        self.addr = addr
    
    def parseData(self, addr):
        self.data = []
        for p in self.parts[1:]:
            if type(p) is int:
                self.data.append(p)
            else:
                for x in p:
                    self.data.append(ord(x))
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
        lines.append(line)
    return lines

def firstPass(lines):
    linesRes = []
    labels = {}
    addr = 0
    for line in lines:
        label = line.stripLabel()
        if label != None:
            labels[label.lower()] = addr
        line.splitParts()
        if len(line.parts) == 0:
            continue
        if line.isCode():
            line.parseInstruction(addr)
        else:
            line.parseData(addr)
        addr += line.size
        linesRes.append(line)
    return linesRes, labels


def secondPass(lines, labels):
    prg = {}
    top = 0
    for line in lines:
        top = max(top, line.addr + line.size)
        if not line.isCode():
            for offset in range(len(line.data)):
                prg['d' + str(line.addr + offset)] = line.data[offset]
            continue
        cntParams = len(line.params)
        for j in range(cntParams):
            p = line.params[j]
            if type(p) is str:
                if p in labels:
                    line.params[j] = labels[p]
                elif p[0] == 'r':
                    line.params[j] = int(p[1:])
        prg[line.addr] = line
        prg['_top'] = top
    return prg

def translate(src):
    lines = prepareLines(src)
    lines, labels = firstPass(lines)
    prg = secondPass(lines, labels)
    return prg

