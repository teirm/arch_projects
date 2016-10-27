#!/usr/bin/python
"""
Project: xsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    22 October 2016
"""

import sys
import json

from pprint import pprint
from bitstring import Bits

# DEFINES
WORD_SIZE = 16

# GLOBALS
REGISTER_FILE = {}
DATA_MEMORY = {}
STATISTICS_DICT = {}


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


def update_register_statistics(dest_register, value):
    """Updates the values in the register file
       for output statistics.

       Keyword arguments:
       dest_register -- the destination register for the
                        value
       value -- the value to place in the destination
                 register

        Return: None
    """
    STATISTICS_DICT['registers'][0][dest_register] = value


def get_register_stats(source_register):
    """Acquires the int value from the stats dict

       Keyword arguments:
       source_register -- the register value desired

       Return: None
    """
    return STATISTICS_DICT['registers'][0][source_register]


def init_statistics_dict():
    """Initializes the statistics dictionary as a
       JSON dictionary.

       Keyword arguments:
       None

       Return: Dictionary
    """
    STATISTICS_DICT['registers'] = [
        {'r0': 0,
         'r1': 0,
         'r2': 0,
         'r3': 0,
         'r4': 0,
         'r5': 0,
         'r6': 0,
         'r7': 0, }
    ]

    STATISTICS_DICT['stats'] = [
        {'add': 0, 'sub': 0, 'and': 0,
         'nor': 0, 'div': 0, 'mul': 0,
         'mod': 0, 'exp': 0, 'lw': 0,
         'sw': 0, 'liz': 0, 'lis': 0,
                            'lui': 0, 'bp': 0, 'bn': 0,
                            'bx': 0, 'bz': 0, 'jr': 0,
                            'jalr': 0, 'j': 0, 'halt': 0,
                            'put': 0,
                            'instructions': 0,
                            'cycles': 0, }
    ]


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
    update_register_statistics(Rd, result)
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
    update_register_statistics(Rd, result)
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

    int_result = Bits(bin=REGISTER_FILE[Rd]).bin
    update_register_statistics(Rd, int_result)
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
    int_result = Bits(bin=REGISTER_FILE[Rd]).bin
    update_register_statistics(Rd, int_result)
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
    update_register_statistics(Rd, int(result))
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
    update_register_statistics(Rd, result)

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
    update_register_statistics(Rd, result)
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
    stored_result = Bits(bin=REGISTER_FILE[Rd]).int
    update_register_statistics(Rd, stored_result)

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
    result = DATA_MEMORY[REGISTER_FILE[Rs].zfill(16)]
    if result > 0:
        REGISTER_FILE[Rd] = Bits(uint=result, length=16).bin
    else:
        REGISTER_FILE[Rd] = Bits(int=result, length=16).bin

    update_register_statistics(Rd, result)

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
    DATA_MEMORY[REGISTER_FILE[Rs].zfill(16)] = get_register_stats(Rt)

    return DATA_MEMORY[REGISTER_FILE[Rs]]


def liz(data_fields):
    """LIS instruction with op_code 01001.  Source is
       word_alligned

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    REGISTER_FILE[Rd] = Imm8.zfill(16)
    int_value = Bits(bin=REGISTER_FILE[Rd]).int
    update_register_statistics(Rd, int_value)
    return REGISTER_FILE[Rd]


def lis(data_fields):
    """LIS instruction with op_code 01001.  Source is
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
    int_value = Bits(bin=REGISTER_FILE[Rd]).int
    update_register_statistics(Rd, int_value)
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
    update_register_statistics(Rd, REGISTER_FILE[Rd])
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

    if check_value > 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return int(ls_bin.int / WORD_SIZE)
    else:
        return program_counter + 1


def branch_negative(data_fields, program_counter):
    """BN instruction with op_code 10101

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int

    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int

    if check_value < 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return int(ls_bin.int / WORD_SIZE)
    else:
        return program_counter + 1


def branch_nzero(data_fields, program_counter):
    """BNZ instruction with op_code 100110

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    (Rd, Imm8) = process_I_instruction(data_fields)
    check_value = Bits(bin=REGISTER_FILE[Rd]).int

    if check_value is not 0:
        z_ext = Imm8.zfill(16)
        ls_bin = Bits(bin=z_ext) << 1
        return int(ls_bin.int / WORD_SIZE)
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
        return int(ls_bin.int / WORD_SIZE)
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
    return int(Bits(bin=REGISTER_FILE[Rs]).int / WORD_SIZE)


def jump_and_link_register(data_fields, program_counter):
    """JALR instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    REGISTER_FILE[Rd] = Bits(
        int=(
            program_counter +
            1) *
        WORD_SIZE,
        length=16).bin
    return int(Bits(bin=REGISTER_FILE[Rs]).int / WORD_SIZE)


def jump_immediate(Imm11, program_counter):
    """JIMM instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]
    program_counter -- the current value of PC

    Return: int
    """
    pc_bits = Bits(int=program_counter, length=16).bin
    ls_imm = Bits(bin=Imm11) << 1
    cat_bits = ''.join([pc_bits[0:5], ls_imm.bin])
    return int(Bits(bin=cat_bits).int / WORD_SIZE)


def put_register(data_fields):
    """PUT instruction with op_code 10011

    Keyword arguments:
    data_fields -- the current instruction being parsed sans
                   the op_code [0:5]

    Return: int
    """
    (Rd, Rs, Rt) = process_R_instruction(data_fields)
    int_value = get_register_stats(Rs)
    print(int_value)  
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
    latency_dict = configure_latency(config_file)
    instruction_memory = parse_input(input_file)
    init_statistics_dict()
    init_register_file()
    program_counter = 0
    clock_cycles = 0
    instruction_count = 0

    while True:
        current_instruction = instruction_memory[program_counter]
        op_code = current_instruction[0:5]
        data_fields = current_instruction[5:16]
        instruction_count += 1

        if op_code == '00000':
            add_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['add']
            STATISTICS_DICT['stats'][0]['add'] += 1
            print('ADD')
        elif op_code == '00001':
            sub_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['sub']
            STATISTICS_DICT['stats'][0]['sub'] += 1
            print('SUB')
        elif op_code == '00010':
            and_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['and']
            STATISTICS_DICT['stats'][0]['and'] += 1
            print('AND')
        elif op_code == '00011':
            nor_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['nor']
            STATISTICS_DICT['stats'][0]['nor'] += 1
            print('NOR')
        elif op_code == '00100':
            div_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['div']
            STATISTICS_DICT['stats'][0]['div'] += 1
            print('DIV')
        elif op_code == '00101':
            mul_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['mul']
            STATISTICS_DICT['stats'][0]['mul'] += 1
            print('MUL')
        elif op_code == '00110':
            mod_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['mod']
            STATISTICS_DICT['stats'][0]['mod'] += 1
            print('MOD')
        elif op_code == '00111':
            exp_instruction(data_fields)
            program_counter += 1
            clock_cycles += latency_dict['exp']
            STATISTICS_DICT['stats'][0]['exp'] += 1
            print('EXP')
        elif op_code == '01000':
            load_word(data_fields)
            program_counter += 1
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['lw'] += 1
            print('LW')
        elif op_code == '01001':
            store_word(data_fields)
            program_counter += 1
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['sw'] += 1
            print('SW')
        elif op_code == '10000':
            liz(data_fields)
            program_counter += 1
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['liz'] += 1
            print('LIZ')
        elif op_code == '10001':
            lis(data_fields)
            program_counter += 1
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['lis'] += 1
            print('LIS')
        elif op_code == '10010':
            lui(data_fields)
            program_counter += 1
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['lui'] += 1
            print('LUI')
        elif op_code == '10100':
            program_counter = branch_positive(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['bp'] += 1
            print('BP')
        elif op_code == '10101':
            program_counter = branch_negative(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['bn'] += 1
            print('BN')
        elif op_code == '10110':
            program_counter = branch_nzero(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['bx'] += 1
            print('BX')
        elif op_code == '10111':
            program_counter = branch_zero(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['bz'] += 1
            print('BZ')
        elif op_code == '01100':
            program_counter = jump_register(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['jr'] += 1
            print('JR')
        elif op_code == '10011':
            program_counter = jump_and_link_register(
                data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['jalr'] += 1
            print('JALR')
        elif op_code == '11000':
            program_counter = jump_immediate(data_fields, program_counter)
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['j'] += 1
            print('J')
        elif op_code == '01101':
            print('HALT')
            clock_cycles += 1
            STATISTICS_DICT['stats'][0]['halt'] += 1
            break
        elif op_code == '01110':
            put_register(data_fields) 
            print('PUT')
            clock_cycles += 1
            program_counter += 1
            STATISTICS_DICT['stats'][0]['put'] += 1
        else:
            print('ERROR: UNRECOGNZIED OPCODE {}'.format(op_code),
                  file=sys.stderr)
            break

    STATISTICS_DICT['stats'][0]['instructions'] = instruction_count
    STATISTICS_DICT['stats'][0]['cycles'] = clock_cycles

    with open(output_file, 'w') as ofp:
        json.dump(STATISTICS_DICT, ofp)

if __name__ == '__main__':

    if len(sys.argv) is not 4:
        print("Usage: ./xsim inputfile configfile outputstatsfile")
        exit(1)

    INPUT_FILE = sys.argv[1]
    CONFIG_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    xsim(CONFIG_FILE, INPUT_FILE, OUTPUT_FILE)
