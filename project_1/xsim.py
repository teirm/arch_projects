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
                binary_value = bin(int(line, 16))[2:].zfill(len(line) * 3)
                instruction_memory.append(binary_value)

    return instruction_memory

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
    data_memory = {}
    program_counter = 0

    while True:
        current_instruction = instruction_memory[program_counter]
        
        if current_instruction[0:5] is '00000':       
            print("FISH")



if __name__ == "__main__":

    if len(sys.argv) is not 4:
        print("Usage: ./xsim inputfile configfile outputstatsfile")
        exit(1)

    CONFIG_FILE = sys.argv[1]
    INPUT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    xsim(CONFIG_FILE, INPUT_FILE, OUTPUT_FILE)
