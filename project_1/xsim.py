#!/usr/bin/python
"""
Project: xsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date: 22 October 2016
"""

import sys
import json
from pprint import pprint


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

       Keywor arguments:
       None

       Return: Dictionary
    """
    
    return {'r0':0,
            'r1':0,
            'r2':0,
            'r3':0,
            'r4':0,
            'r5':0,
            'r6':0,
            'r7':0,}


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
    register_file = init_register_file()
    data_memory = {}
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

        program_counter += 1

if __name__ == '__main__':

    if len(sys.argv) is not 4:
        print("Usage: ./xsim inputfile configfile outputstatsfile")
        exit(1)

    CONFIG_FILE = sys.argv[1]
    INPUT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    xsim(CONFIG_FILE, INPUT_FILE, OUTPUT_FILE)
