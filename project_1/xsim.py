#!/usr/bin/python
"""
Project: xsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date: 22 October 2016
"""

import sys
import json

from bitstring import Bits

REGISTER_FILE = {}
DATA_MEMORY = {}


def configure_latency(config_file):
    """Configures the latencies for the processor simulation
        from a JSON input file

        Keyword arguments:
        config_file -- JSON file containing latency configurations

        Return: dictionary
    """
    latency_values = {'add': 1,
                      'sub': 1,
                      'and': 1,
                      'nor': 1,
                      'div': 1,
                      'mul': 1,
                      'mod': 1,
                      'exp': 1}

    with open(config_file) as configuration:
        config_values = json.load(configuration)

    for key in config_values.keys():
        latency_values[key] = config_values[key]

    return latency_values


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


def init_register_file():
    """Initializes the register file prior to
       simulation.

       Keyword arguments:
       None

       Return: Dictionary
    """

    REGISTER_FILE['r0'] = ''.zfill(16)
    REGISTER_FILE['r1'] = ''.zfill(16)
    REGISTER_FILE['r2'] = ''.zfill(16)
    REGISTER_FILE['r3'] = ''.zfill(16)
    REGISTER_FILE['r4'] = ''.zfill(16)
    REGISTER_FILE['r5'] = ''.zfill(16)
    REGISTER_FILE['r6'] = ''.zfill(16)
    REGISTER_FILE['r7'] = ''.zfill(16)


def init_statistics_dict():
    """Initializes the statistics dictionary as a
       JSON dictionary.

       Keyword arguments:
       None

       Return: Dictionary
    """
    return {'registers':
            [
                {'r0': 0,
                 'r1': 0,
                 'r2': 0,
                 'r3': 0,
                 'r4': 0,
                 'r5': 0,
                 'r6': 0,
                 'r7': 0, }
            ],
            'stats':
                [
                    {'add': 0, 'sub': 0, 'and': 0,
                     'nor': 0, 'div': 0, 'mul': 0,
                     'mod': 0, 'exp': 0, 'lw': 0,
                     'sw': 0, 'liz': 0, 'lis': 0,
                     'lui': 0, 'bp': 0, 'bn': 0,
                     'bx': 0, 'bz': 0, 'jr': 0,
                     'jal': 0, 'j': 0, 'halt': 1,
                     'put': 0,
                     'instructions': 0,
                     'cycles': 0, }
            ]
            }


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


def add_instruction(data_fields):
    """ADD instruction with op_code '00000'

    Keyword arguments:
    data_fields -- the current instruction being parsed
                  sans the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int + Bits(bin=REGISTER_FILE[Rt]).int
    REGISTER_FILE[Rd] = Bits(int=result, length=16).bin
    return REGISTER_FILE[Rd]


def sub_instruction(data_fields):
    """SUB instruction with op_code '00001'

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int - Bits(bin=REGISTER_FILE[Rt]).int
    REGISTER_FILE[Rd] = Bits(int=result, length=16).bin
    return REGISTER_FILE[Rd]


def and_instruction(data_fields):
    """AND instruction with op_code '00010'

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    REGISTER_FILE[Rd] = (
        Bits(
            bin=REGISTER_FILE[Rs]) & Bits(
            bin=REGISTER_FILE[Rt])).bin
    return REGISTER_FILE[Rd]


def nor_instruction(data_fields):
    """NOR instruction with op_code '00011'

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int

    NOTE: POTENTIAL BUG DUE TO TWOS-COMPLEMENT
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    REGISTER_FILE[Rd] = (~(Bits(bin=REGISTER_FILE[Rs]) |
                           Bits(bin=REGISTER_FILE[Rt]))).bin
    return REGISTER_FILE[Rd]


def div_instruction(data_fields):
    """DIV instruction with op_code '00100'

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int / Bits(bin=REGISTER_FILE[Rt]).int
    REGISTER_FILE[Rd] = Bits(int=int(result), length=16).bin
    return REGISTER_FILE[Rd]


def mul_instruction(data_fields):
    """MUL instruction with op_code '00100'.  Takes only
       lower 16 bits of result

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int * Bits(bin=REGISTER_FILE[Rt]).int
    bin_result = Bits(int=result, length=32).bin
    REGISTER_FILE[Rd] = bin_result[len(bin_result) - 16:len(bin_result)]

    return REGISTER_FILE[Rd]


def mod_instruction(data_fields):
    """MOD instruction with op_code '00110'.

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int % Bits(bin=REGISTER_FILE[Rt]).int
    REGISTER_FILE[Rd] = Bits(int=result, length=16).bin
    return REGISTER_FILE[Rd]


def exp_instruction(data_fields):
    """EXP instruction with op_code '00111'.

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    result = Bits(bin=REGISTER_FILE[Rs]).int ** Bits(bin=REGISTER_FILE[Rt]).int
    bin_result = Bits(int=result, length=32).bin
    REGISTER_FILE[Rd] = bin_result[len(bin_result) - 16:len(bin_result)]

    return REGISTER_FILE[Rd]


def load_word(data_fields):
    """LW instruction with op_code 01000.  Source is
       word_alligned

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    REGISTER_FILE[Rd] = DATA_MEMORY[REGISTER_FILE[Rs].zfill(16)]

    return REGISTER_FILE[Rd]


def store_word(data_fields):
    """SW instruction with op_code 01001.  Source is
       word_alligned

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    DATA_MEMORY[REGISTER_FILE[Rs].zfill(16)] = REGISTER_FILE[Rt]
    return DATA_MEMORY[REGISTER_FILE[Rs]]


def liz(data_fields):
    """SW instruction with op_code 01001.  Source is
       word_alligned

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int

    NOTE: POSSIBLE ERROR DUE TO TWOs COMPLEMENT
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    REGISTER_FILE[Rd] = Imm8.zfill(16)
    return REGISTER_FILE[Rd]


def lis(data_fields):
    """SW instruction with op_code 01001.  Source is
       word_alligned

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int

    NOTE: POSSIBLE ERROR DUE TO TWOs COMPLEMENT
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    msb = Imm8[0]
    REGISTER_FILE[Rd] = Imm8.rjust(16, msb)
    print(REGISTER_FILE[Rd])
    return REGISTER_FILE[Rd]


def lui(data_fields):
    """LUI instruction with op_code 10010

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int

    NOTE: POSSIBLE ERROR DUE TO TWOs COMPLEMENT
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    REGISTER_FILE[Rd] = ''.join([Imm8,
                                 Bits(bin=REGISTER_FILE[Rd][8:16]).bin])
    return REGISTER_FILE[Rd]


def branch_positive(data_fields, program_counter):
    """BP instruction with op_code 10100

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int
    print(check_value)

    if check_value > 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return program_counter + ls_bin.int
    else:
        return program_counter + 1


def branch_negative(data_fields, program_counter):
    """BN instruction with op_code 10101

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int

    NOTE: UNSURE ABOUT RETURN PC+2
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int

    if check_value < 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return program_counter + ls_bin.int
    else:
        return program_counter + 1


def branch_nzero(data_fields, program_counter):
    """BNZ instruction with op_code 100110

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int

    NOTE: UNSURE ABOUT RETURN PC+2
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int

    if check_value is not 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return program_counter + ls_bin.int
    else:
        return program_counter + 1


def branch_zero(data_fields, program_counter):
    """BNZ instruction with op_code 100111

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int

    NOTE: UNSURE ABOUT RETURN PC+2
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int

    if check_value is 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return program_counter + ls_bin.int
    else:
        return program_counter + 1


def jump_register(data_fields, program_counter):
    """JR instruction with op_code 01100

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    return program_counter + Bits(bin=REGISTER_FILE[Rs]).int


def jump_and_link_register(data_fields, program_counter):
    """JALR instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    REGISTER_FILE[Rd] = Bits(int=program_counter + 1, length=16).bin
    return (Bits(bin=REGISTER_FILE[Rs]) << 1).int


def jump_immediate(Imm11, program_counter):
    """JALR instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    pc_bits = Bits(int=program_counter, length=16).bin
    print(pc_bits)
    ls_imm = Bits(bin=Imm11) << 1
    print(ls_imm.bin)
    cat_bits = ''.join([pc_bits[0:5], ls_imm.bin])
    return Bits(bin=cat_bits).int


def put_register(data_fields):
    """PUT instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    print(REGISTER_FILE[Rs])
    return REGISTER_FILE[Rs]


def xsim(config_file, input_file, output_file):
    """Run the simulation of the X isa for given
       configuration and input file and maintain stats

       Keyword arguments:
       config_file -- JSON file containing latency configurations
       input_file -- list of instructions and comments in ASCII Hex
       output_file -- output file for simulation statistics

       Return: None
    """
    statistics_dict = init_statistics_dict()
    latency_dict = configure_latency(config_file)
    instruction_memory = parse_input(input_file)
    init_register_file()
    program_counter = 0

    while True:
        current_instruction = instruction_memory[program_counter]
        op_code = current_instruction[0:5]

        if op_code == '00000':
            print('ADD')
        elif op_code == '00001':
            print('SUB')
        elif op_code == '00010':
            print('AND')
        elif op_code == '00011':
            print('NOR')
        elif op_code == '00101':
            print('DIV')
        elif op_code == '00110':
            print('MUL')
        elif op_code == '00111':
            print('EXP')
        elif op_code == '01000':
            print('LW')
        elif op_code == '01001':
            print('SW')
        elif op_code == '10000':
            print('LIZ')
        elif op_code == '10001':
            print('LIS')
        elif op_code == '10010':
            print('LUI')
        elif op_code == '10100':
            print('BP')
        elif op_code == '10101':
            print('BN')
        elif op_code == '10110':
            print('BX')
        elif op_code == '10111':
            print('BZ')
        elif op_code == '01100':
            print('JR')
        elif op_code == '10011':
            print('JALR')
        elif op_code == '11000':
            print('J')
        elif op_code == '01101':
            print('HALT')
            break
        elif op_code == '01110':
            print('PUT')
        else:
            print('ERROR: UNRECOGNZIED OPCODE {}'.format(op_code),
                  file=sys.stderr)
            break

    with open(output_file, 'w') as ofp:
        json.dump(statistics_dict, ofp)

if __name__ == '__main__':

    if len(sys.argv) is not 4:
        print("Usage: ./xsim inputfile configfile outputstatsfile")
        exit(1)

    CONFIG_FILE = sys.argv[1]
    INPUT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    xsim(CONFIG_FILE, INPUT_FILE, OUTPUT_FILE)
