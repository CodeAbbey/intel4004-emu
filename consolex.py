import sys

class Consolex:
    
    def c_3f0(self):
        v = ord(sys.stdin.read(1))
        self.regs[1] = v & 0xF
        self.regs[0] = v >> 4

    def c_3e0(self):
        v = (self.regs[0] << 4) + self.regs[1]
        sys.stdout.write(chr(v))
