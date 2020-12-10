import time
import math
from PEC import MCP

mcp = MCP()

class Motor:

    def __init__(self, reg):
        self.reg = reg
        self.output = [reg, '0', '0', '0', '0', '0', '0', '0', '0']
        out = ''
        for i in self.output:
            out = out + i
        mcp.output(out)

        self.curr_step0 = 0
        self.curr_step1 = 0

        self.direction0 = 0
        self.direction1 = 0

        self.step_seq = [
            '1000',
            '1010',
            '0010',
            '0110',
            '0100',
            '0101',
            '0001',
            '1001'
        ]

    def get_steps(self):
        return [self.curr_step0, self.curr_step1]

    def set_curr_step(self, step0, step1):
        self.curr_step0 = step0
        self.curr_step1 = step1

    def move_step0(self, direction):
        self.curr_step0 -= direction
        if self.curr_step0 > 7:
            self.curr_step0 = 0
        if self.curr_step0 < 0:
            self.curr_step0 = 7

        self.curr_step0 = int(self.curr_step0)
        out = ''
        for i in range(4):
            self.output[i+1] = self.step_seq[self.curr_step0][i]
        for i in self.output:
            out = out + i
        mcp.output(out)
                
    def move_step1(self, direction):
        self.curr_step1 += direction
        if self.curr_step1 > 7:
            self.curr_step1 = 0
        if self.curr_step1 < 0:
            self.curr_step1 = 7

        self.curr_step1 = int(self.curr_step1)
        out = ''
        for i in range(4):
            self.output[i+5] = self.step_seq[self.curr_step1][i]
        for i in self.output:
            out = out + i
        mcp.output(out)


    def off0(self):
        out = ''
        for i in range(4):
            self.output[i+1] = '0'
        for i in self.output:
            out = out + i
        mcp.output(out)
    def off1(self):
        out = ''
        for i in range(4):
            self.output[i+5] = '0'
        for i in self.output:
            out = out + i
        mcp.output(out)
    def on0(self):
        out = ''
        for i in range(4):
            self.output[i+1] = self.step_seq[self.curr_step0][i]
        for i in self.output:
            out = out + i
        mcp.output(out)
    def on1(self):
        out = ''
        for i in range(4):
            self.output[i+5] = self.step_seq[self.curr_step1][i]
        for i in self.output:
            out = out + i
        mcp.output(out)