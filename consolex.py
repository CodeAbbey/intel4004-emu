import sys

class Consolex:
    
    def c_3f0(self):
        ch = sys.stdin.read(1)
        v = ord(ch) if len(ch) > 0 else 0
        self.regs[1] = v & 0xF
        self.regs[0] = v >> 4

    def c_3e0(self):
        v = (self.regs[0] << 4) + self.regs[1]
        sys.stdout.write(chr(v))
