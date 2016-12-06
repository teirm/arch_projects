#!/usr/bin/python
"""
Project: tomsim
Modulue: assembler
Date: 26 Nov 2016
Author: Cyrus Ramavarapu
"""

import sys
from pprint import pprint
from bitstring import Bits

OP_CODES = {'00000': 'add',
            '00001': 'sub',
            '00010': 'and',
            '00011': 'nor',
            '00100': 'div',
            '00101': 'mul',
            '00110': 'mod',
            '00111': 'exp',
            '01000': 'lw',
            '01001': 'sw',
            '10000': 'liz',
            '10001': 'lis',
            '10010': 'lui',
            '10100': 'bp',
            '10101': 'bn',
            '10110': 'bx',
            '10111': 'bz',
            '01100': 'jr',
            '10011': 'jalr',
            '11000': 'j',
            '01101': 'halt',
            '01110': 'put'}

REGISTER_FILE = {'000': 'r0',
                 '001': 'r1',
                 '010': 'r2',
                 '011': 'r3',
                 '100': 'r4',
                 '101': 'r5',
                 '110': 'r6',
                 '111': 'r7'}

REGISTER_FILE = {v.upper(): k for k, v in REGISTER_FILE.items()}
OP_CODES = {v.upper(): k for k, v in OP_CODES.items()}


def parse_triple(instr_values):
    """Parses instructions with 3 ops"""

    instr_bits = OP_CODES[instr_values[0]]
    rd_bits = REGISTER_FILE[instr_values[1]]
    rs_bits = REGISTER_FILE[instr_values[2]]
    rt_bits = REGISTER_FILE[instr_values[3]]

    bin_string = ''.join([instr_bits, rd_bits, rs_bits, rt_bits, '00'])

    return hex(int(bin_string, 2))[2:].zfill(4)


def parse_double(instr_values):
    """Parses instructions with 2 ops"""

    if instr_values[0] == 'LW':
        instr_bits = OP_CODES[instr_values[0]]
        rd_bits = REGISTER_FILE[instr_values[1]]
        rs_bits = REGISTER_FILE[instr_values[2]]
        rt_bits = '00000'

        bin_string = ''.join([instr_bits, rd_bits, rs_bits, rt_bits])

        print('LW')
        print(bin_string)

    elif instr_values[0] == 'SW':
        instr_bits = OP_CODES[instr_values[0]]
        rd_bits = '000'
        rs_bits = REGISTER_FILE[instr_values[1]]
        rt_bits = REGISTER_FILE[instr_values[2]]

        bin_string = ''.join([instr_bits, rd_bits, rs_bits, rt_bits, '00'])

        print('SW')
        print(bin_string)
    else:
        instr_bits = OP_CODES[instr_values[0]]
        rd_bits = REGISTER_FILE[instr_values[1]]
        imm8_bits = Bits(int=int(instr_values[2], 10), length=8).bin
        bin_string = ''.join([instr_bits, rd_bits, imm8_bits])

    return hex(int(bin_string, 2))[2:].zfill(4)


def parse_single(instr_values):
    """Parses instructions with 1 ops"""

    instr_bits = OP_CODES[instr_values[0]]
    rd_bits = '000'
    rs_bits = REGISTER_FILE[instr_values[1]]
    rt_bits = '00000'

    bin_string = ''.join([instr_bits, rd_bits, rs_bits, rt_bits])

    return hex(int(bin_string, 2))[2:].zfill(4)


def parse_asm_file(asm_file):
    """Parses the assembly file and outputs
    a list of tuples for each instruction"""

    hex_code = []

    triple_type = ['ADD', 'SUB', 'AND', 'NOR',
                   'DIV', 'MUL', 'MOD', 'EXP']

    double_type = ['LW', 'SW', 'LIZ', 'LIS',
                   'LUI']

    single_type = ['PUT']

    with open(asm_file, 'r') as assembly:
        for line in assembly:
            line = line.strip()
            line = line.replace(',', '')
            line = line.upper()
            instr_values = line.split(' ')

            if instr_values[0] in triple_type:
                hex_val = parse_triple(instr_values)
            elif instr_values[0] in double_type:
                hex_val = parse_double(instr_values)
            elif instr_values[0] in single_type:
                hex_val = parse_single(instr_values)
            else:
                hex_val = '6800'

            hex_code.append(hex_val.upper())

    return hex_code


def assembler(asm_file, out_file):
    """Simple assembler used for ISA x and
    tom sim testing"""

    hex_values = parse_asm_file(asm_file)

    pprint(hex_values)

    with open(out_file, 'w') as ofp:
        for element in hex_values:
            print(element, file=ofp)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: ./assembler.py input.dis output.hex')
        sys.exit(-1)

    ASM_FILE = sys.argv[1]
    OUT_FILE = sys.argv[2]

    assembler(ASM_FILE, OUT_FILE)
