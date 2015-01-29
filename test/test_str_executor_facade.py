import unittest

import sys
import os
import io

if __name__ == '__main__':
    sys.path.append(os.path.abspath('..'))  # using test without package

from intel4004_emu.str_executor_facade import StrExecutorFacade, StrExecutorFacadeDebug


class TestStrExecutorFacade(unittest.TestCase):

    def test_examples(self):
        cpu = StrExecutorFacade()
        cpu.load_assembly('''\
        ldm 5
        xch r2''')
        self.assertEqual('0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

        cpu.load_assembly('''\
        ldm 5
        xch r2
        ldm 3
        xch r2
        xch r1
        ''')
        self.assertEqual('0 5 3 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

        cpu.load_assembly('''\
        start:
          iac
          xch r1
        finish:
          nop
        ''')
        self.assertEqual('0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

        cpu.load_assembly('''\
        fim r0 $31
        fim r2 $41
        fim r4 $59
        fim r6 $26
        fim r12 250
        fim r14 206
        ''')
        self.assertEqual('3 1 4 1 5 9 2 6 0 0 0 0 f a c e', cpu.run().regs2str)

        cpu.load_assembly('''\
        ldm 6
        ral
        xch r0

        ldm 8
        rar
        xch r1

        ldm 7
        rar
        rar
        xch r2
        ''')
        self.assertEqual('c 4 9 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

        cpu.load_assembly('''\
        ldm 5
        xch r0
        jun skip_few
        ldm 6
        xch r1
        skip_few:
        ldm 7
        xch r2
        ''')
        self.assertEqual('5 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

        cpu.load_assembly('''\
        ldm 0
        xch r0

        jms add_three
        jms add_three
        jms add_three
        jun finish

        add_three:
        ld r0
        iac
        iac
        iac
        xch r0
        bbl 0

        finish:
        nop
        ''')
        self.assertEqual('9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0', cpu.run().regs2str)

    def test_clear(self):
        cpu = StrExecutorFacade('''\
        add r0
        add r0
        ''')
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1',
                         cpu.run('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0').regs2str_ex)
        cpu.load_assembly('')
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1',
                         cpu.run(clear=False).regs2str_ex)

        cpu = StrExecutorFacade('''\
        add r0
        ''')
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=8, cy=0',
                         cpu.run('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0').regs2str_ex)
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1',
                         cpu.run(clear=False).regs2str_ex)
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=9, cy=0',
                         cpu.run(clear=False).regs2str_ex)

    def test_debug(self):
        out = io.StringIO()
        sys.stdout = out
        cpu = StrExecutorFacadeDebug('''\
        add r0
        add r0
        ''')
        self.assertEqual('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1',
                         cpu.run('8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0').regs2str_ex)
        self.assertEqual('''\
Before:          8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0
0: add 0         8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=8, cy=0
1: add 0         8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1
''', out.getvalue())

    def test_run_multiple_times(self):
        cpu = StrExecutorFacade('''\
        xch r1
        rar
        xch r1
        ''')
        for state, res in [
            ('0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 a 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 b 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 c 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 d 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
            ('0 e 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=0'),
            ('0 f 0 0 0 0 0 0 0 0 0 0 0 0 0 0', '0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0, acc=0, cy=1'),
        ]:
            self.assertEqual(res, cpu.run(state).regs2str_ex)

    def test_console(self):
        cpu = StrExecutorFacade('''\
        jms $3f0
        jms $3e0
        ''')
        self.assertEqual('A', cpu.run(console='A').console_output)
        cpu = StrExecutorFacade('''\
        loop:
        jms $3f0
        ld r2
        jcn az exit
        inc r3
        jms $3e0
        jun loop
        exit:
        ''')
        self.assertEqual('BCD', cpu.run(console='ABC').console_output)


if __name__ == '__main__':
    unittest.main()