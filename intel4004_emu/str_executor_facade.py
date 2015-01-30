from intel4004_emu import executor
from intel4004_emu import translator


class ExecutorExt(executor.Executor):
    def __init__(self):
        super(executor.Executor, self).__init__()
        self.console_input = []
        self.console_output = []

    def clear_memory(self):
        self.acc = 0
        self.regs = [0] * 16
        self.cy = 0
        self.memory = [0] * 256

    def clear_stack(self):
        self.dp = 0
        self.ip = 0
        self.stack = []
        self.console_input = []
        self.console_output = []

    @property
    def regs2str(self):
        return ' '.join('{:x}'.format(x) for x in self.regs)

    @property
    def regs2str_ex(self):
        return '{}, acc={}, cy={}'.format(' '.join('{:x}'.format(x) for x in self.regs), self.acc, self.cy)

    def c_3f0(self):
        if self.console_input:
            v = ord(self.console_input.pop(0))
        else:
            v = 0
        self.regs[3] = v & 0xF
        self.regs[2] = v >> 4

    def c_3e0(self):
        v = (self.regs[2] << 4) + self.regs[3]
        self.console_output.append(chr(v))


class StrExecutorFacade(object):
    executor_class = ExecutorExt

    def __init__(self, src=None):
        self.cpu = self.executor_class()
        self.prg = None
        if src is not None:
            self.load_assembly(src)

    def load_assembly(self, src):
        self.prg = translator.translate(src.splitlines())

    def run(self, state=None, console=None, clear=True):
        if self.prg is None:
            raise RuntimeError('Program is not loaded. Execute load_assembly() before.')
        self.cpu.clear_stack()
        if clear:
            self.cpu.clear_memory()
        if console:
            self.cpu.console_input = list(console)
        if state is not None:
            self.cpu.regs = [int(x, 16) for x in state.split()]
        self.cpu.run(self.prg)
        return self

    @property
    def regs2str(self):
        return self.cpu.regs2str

    @property
    def regs2str_ex(self):
        return self.cpu.regs2str_ex

    @property
    def console_output(self):
        return ''.join(self.cpu.console_output)


class ExecutorExtDebug(ExecutorExt):

    def step(self, line):
        super().step(line)
        print('{:<16} {}'.format(str(line), self.regs2str_ex))

    def run(self, prg, limit=50):
        i = 0
        print('Before:          {}'.format(self.regs2str_ex))
        while self.ip in prg:
            self.step(prg[self.ip])
            i += 1
            if i > limit:
                break


class StrExecutorFacadeDebug(StrExecutorFacade):
    executor_class = ExecutorExtDebug
