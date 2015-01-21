class Executor:
    
    def __init__(self):
        self.acc = 0
        self.regs = [0] * 16
        self.cy = 0
        self.ip = 0
        self.stack = []
    
    def run(self, prg):
        while self.ip in prg:
            self.step(prg[self.ip])
        self.printRegs()
    
    def printRegs(self):
        print(' '.join([str(r) for r in self.regs]))
        print("acc=%d, cy=%d, ip=%d" % (self.acc, self.cy, self.ip))
    
    def step(self, line):
        self.ip += line.size
        cmd = getattr(self, 'i_' + line.opcode)
        cmd(line.params)
    
    def i_add(self, params):
        p = params[0]
        self.acc = self.acc + self.regs[p] + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
        
    def i_bbl(self, params):
        self.ip = self.stack.pop()
        self.acc = params[0] & 0xF
    
    def i_clb(self, params):
        self.acc = 0
        self.cy = 0
        
    def i_clc(self, params):
        self.cy = 0
        
    def i_cma(self, params):
        self.acc ^= 0xF
        
    def i_cmc(self, params):
        self.cy ^= 1
        
    def i_dac(self, params):
        self.aac = (self.acc - 1) & 0xF
    
    def i_fim(self, params):
        p = params[0] & 0xE
        v = params[1]
        self.regs[p] = (v >> 4) & 0xF
        self.regs[p + 1] = v & 0xF
            
    def i_iac(self, params):
        self.acc = (self.acc + 1) & 0xF
    
    def i_jcn(self, params):
        raise Exception('Unsupported')
    
    def i_jms(self, params):
        self.stack.append(self.ip)
        self.ip = params[0]
    
    def i_inc(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
    
    def i_isz(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
        if self.regs[p] != 0:
            self.ip = params[1]
    
    def i_jun(self, params):
        self.ip = params[0]
    
    def i_ld(self, params):
        self.acc = self.regs[params[0]]
        
    def i_ldm(self, params):
        self.acc = params[0] & 0xF
    
    def i_nop(self, params):
        pass
    
    def i_ral(self, params):
        self.acc = (self.acc << 1) + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_rar(self, params):
        cy = self.acc & 1
        self.acc = (self.acc >> 1) + (self.cy << 3)
        self.cy = cy
    
    def i_stc(self, params):
        self.cy = 1
    
    def i_sub(self, params):
        p = params[0]
        self.acc = self.acc + 16 - self.regs[p] - self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_sub(self, params):
        self.acc = self.cy
        self.cy = 0
    
    def i_xch(self, params):
        p = params[0]
        self.regs[p], self.acc = self.acc, self.regs[p]

