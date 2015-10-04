class Executor(object):
    
    def __init__(self):
        self.acc = 0
        self.regs = [0] * 16
        self.cy = 0
        self.memory = [0] * 256
        self.dp = 0
        self.ip = 0
        self.stack = []
    
    def run(self, prg):
        self.prg = prg
        while self.ip in prg:
            self.step(prg[self.ip])
    
    def step(self, line):
        self.ip += line.size
        cmd = getattr(self, 'i_' + line.opcode)
        cmd(line.params)
    
    def jump(self, param):
        if type(param) != int:
            raise Exception('Label address not resolved: ' + str(param))
        self.ip = param
    
    def i_add(self, params):
        p = params[0]
        self.acc = self.acc + self.regs[p] + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
        
    def i_adm(self, params):
        self.acc = self.acc + self.memory[self.dp] + self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
        
    def i_bbl(self, params):
        self.jump(self.stack.pop())
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
    
    def i_daa(self, params):
        if self.acc >= 10:
            self.cy = 1
            self.acc -= 10
        else:
            self.cy = 0
    
    def i_dac(self, params):
        self.acc = (self.acc - 1) & 0xF
        self.cy = 1 if self.acc != 15 else 0
    
    def i_fim(self, params):
        p = params[0] & 0xE
        v = params[1]
        self.regs[p] = (v >> 4) & 0xF
        self.regs[p + 1] = v & 0xF
    
    def i_fin(self, params):
        p = params[0] & 0xE
        addr = 'd' + str(self.regs[0] * 16 + self.regs[1])
        if addr in self.prg:
            v = self.prg[addr]
            self.regs[p] = (v >> 4) & 0xF
            self.regs[p + 1] = v & 0xF
        else:
            raise Exception("Attempt to read the data from uninitialized ROM address %s" % addr[1:])
            
    def i_iac(self, params):
        self.acc = (self.acc + 1) & 0xF
        self.cy = 1 if self.acc == 0 else 0
    
    def i_jcn(self, params):
        op = params[0]
        if op not in ['c0', 'c1', 'az', 'an']:
            raise Exception("Unknown jump condition '%s'!" % op);
        if op[0] == 'c':
            if str(self.cy) != op[1]:
                return
        elif op == 'az' and self.acc != 0:
            return
        elif op == 'an' and self.acc == 0:
            return
        self.jump(params[1])
    
    def i_jms(self, params):
        addr = params[0]
        if type(addr) != int:
            raise Exception('Subroutine address not resolved: ' + str(addr))
        if addr < 0x300:
            self.stack.append(self.ip)
            self.jump(params[0])
        else:
            try:
                subr = getattr(self, "c_%0.3x" % addr)
            except AttributeError:
                raise Exception("No custom subroutine for address %0.3x was defined!" % addr)
            subr()
    
    def i_jun(self, params):
        self.jump(params[0])
    
    def i_inc(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
    
    def i_isz(self, params):
        p = params[0]
        self.regs[p] = (self.regs[p] + 1) & 0xF
        if self.regs[p] != 0:
            self.jump(params[1])
    
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
    
    def i_rdm(self, params):
        self.acc = self.memory[self.dp]
    
    def i_src(self, params):
        p = params[0] & 0xE
        self.dp = (self.regs[p] << 4) + self.regs[p + 1]
    
    def i_stc(self, params):
        self.cy = 1
    
    def i_sub(self, params):
        p = params[0]
        self.acc = self.acc + self.cy + (self.regs[p] ^ 0xF)
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_sbm(self, params):
        self.acc = self.acc + 16 - self.memory[self.dp] - self.cy
        self.cy = self.acc >> 4
        self.acc &= 0xF
    
    def i_tcc(self, params):
        self.acc = self.cy
        self.cy = 0
    
    def i_tcs(self, params):
        self.acc = 9 + self.cy
        self.cy = 0
    
    def i_wrm(self, params):
        self.memory[self.dp] = self.acc
    
    def i_xch(self, params):
        p = params[0]
        self.regs[p], self.acc = self.acc, self.regs[p]
