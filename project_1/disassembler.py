#!/usr/bin/python
"""
Project: xsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    22 October 2016
"""

import sys
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
            '10100': 'lui',
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


def process_R_instruction(data_fields):
    """Processes R type instruction for ISA X

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: Tuple(Rd, Rs, Rt)

    """
    Rd = ''.join(['r', str(int(data_fields[0:3], 2))])
    Rs = ''.join(['r', str(int(data_fields[3:6], 2))])
    Rt = ''.join(['r', str(int(data_fields[6:9], 2))])

    return (Rd, Rs, Rt)


def parse_input(input_file):
    """Parses input file and converts ASCII
       Hex instructions into binary

       Keyword arguments:
       input_file -- file containing instructions in ASCII hex

       Return: List
    """

    instruction_memory = []

    with open(input_file) as hex_data:
        for line in hex_data:
            if line[0] is not '#':
                binary_value = bin(int(line, 16))[2:].zfill(4 * 4)
                instruction_memory.append(binary_value)

    return instruction_memory


def process_I_instruction(data_fields):
    """Processes I type instruction for ISA X

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: Tuple(Rd, Imm8)
    """
    Rd = ''.join(['r', str(int(data_fields[0:3], 2))])
    Imm8 = data_fields[3:11]

    return (Rd, Imm8)


def disassembler(input_file, out_file):
    """A isa X disassembler

    Keyword arguments:
    file_name -- name of the file containing
                 hex code
    out_file -- name of the output file

    Return: None
    """
    instruction_memory = parse_input(input_file)
    with open(out_file, 'w') as assembly_code:
        for instruction in instruction_memory:
            op_code = instruction[0:5]
            data_fields = instruction[5:16]

            if op_code == '00000':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('ADD {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('ADD')
            elif op_code == '00001':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('SUB {}, {}, {}'.format(
                     Rd, Rs, Rt),
                    file=assembly_code
                )
                print('SUB')
            elif op_code == '00010':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('AND {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('AND')
            elif op_code == '00011':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('NOR {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('NOR')
            elif op_code == '00100':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('DIV {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('DIV')
            elif op_code == '00101':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('MUL {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('MUL')
            elif op_code == '00110':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('MOD {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('MOD')
            elif op_code == '00111':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('EXP {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('EXP')
            elif op_code == '01000':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('LW {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('LW')
            elif op_code == '01001':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('SW {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('SW')
            elif op_code == '10000':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('LIZ {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('LIZ')
            elif op_code == '10001':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).int
                print('LIS {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('LIS')
            elif op_code == '10010':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('LUI {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('LUI')
            elif op_code == '10100':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('BP {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('BP')
            elif op_code == '10101':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('BN {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('BN')
            elif op_code == '10110':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('BX {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('BX')
            elif op_code == '10111':
                (Rd, Imm8) = process_I_instruction(data_fields)
                int_value = Bits(bin=Imm8).uint
                print('BZ {}, {}'.format(
                    Rd, int_value),
                    file=assembly_code
                )
                print('BZ')
            elif op_code == '01100':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('JR {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('JR')
            elif op_code == '10011':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('JALR {}, {}, {}'.format(
                    Rd, Rs, Rt),
                    file=assembly_code
                )
                print('JALR')
            elif op_code == '11000':
                int_value = Bits(bin=data_fields).uint
                print('j {}'.format(int_value), file=assembly_code)
                print('J')
            elif op_code == '01101':
                print('HALT', file=assembly_code)
                print('HALT')
            elif op_code == '01110':
                (Rd, Rs, Rt) = process_R_instruction(data_fields)
                print('PUT {}'.format(Rs), file=assembly_code)
                print('PUT')
            else:
                print('ERROR: UNRECOGNZIED OPCODE {}'.format(op_code),
                      file=sys.stderr)
                break

if __name__ == '__main__':
    FILE_NAME = sys.argv[1]
    OUT_FILE = sys.argv[2]
    disassembler(FILE_NAME, OUT_FILE)
