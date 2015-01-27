import sys

class Consolex:
    
    def c_3f0(self):
        ch = sys.stdin.read(1)
        v = ord(ch) if len(ch) > 0 else 0
        self.regs[3] = v & 0xF
        self.regs[2] = v >> 4

    def c_3e0(self):
        v = (self.regs[2] << 4) + self.regs[3]
        sys.stdout.write(chr(v))
