#!/usr/bin/python
"""
Project: tomsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    19 November 2016
"""

import sys
import json

from pprint import pprint
from bitstring import Bits

# DEFINES
BUSY = 1
FREE = 0

# FUNCTIONAL UNIT ARRAYS
INTEGER = []
DIVIDER = []
MULTIPLIER = []
LOAD = []
STORE = []

# RESERVATION STATION ARRAYS
INT_RS = []
DIV_RS = []
MULT_RS = []
LD_RS = []
ST_RS = []

# RESVERATION STATION MAX LENGTHS
INT_RS_MAX = 0
DIV_RS_MAX = 0
MULT_RS_MAX = 0
LD_RS_MAX = 0
ST_RS_MAX = 0

# RESGISTER RENAMING
RES_RENAME = {}

# RESERVATION STATION STATUS
RES_STATUS = {}

# EVENT QUEUE
EVENT_QUEUE = []

# INSTRUCTION MEMORY

INSTRUCTIONS = []

# Need to store latencies some where
class PipeEvent:
    """Event entry for tomsim to model ISSUE,
    READ_OPERAND, EXECUTE, and WRITE_REGISTER
    """

    def __init__(self, event_type, current_cycle, latency):
        self.event = event_type
        self.dest = None
        self.source_1 = None
        self.source_2 = None
        self.start = current_cycle
        self.end = current_cycle + latency

    def set_sources(self, s1, s2):
        """Sets the sources for the event

        Keyword arguments:
        s1 -- source operand 1 or FU producing
        s2 -- source operand 2 or FU producing

        Returns: None
        """
        self.source_1 = s1
        self.source_2 = s2

    def set_destination(self, dest):
        """Sets the destination for the event

        Keyword arguments:
        dest -- destination FU producing

        Returns: None
        """
        self.dest = None

    def update_event(self, new_event):
        """Updates the event as it moves through
        the event queue

        Keyword arguments:
        new_event -- the new event for this object

        Returns: None
        """
        self.event = new_event

    def get_event(self):
        """Returns the event type

        Keyword arguments:
        None

        Return: String
        """
        return self.event

    def get_sources(self):
        """Returns the sources for the event

        Keyword arguments:
        None

        Return: Tuple of sources
        """
        return (self.source_1, self.source_2)

    def get_age(self, current_cycle):
        """Computes the age of the event based
        on its start cycle and the current cycle

        Keyword arguments:
        current_cycle -- the current cycle of execution

        Return: Int
        """
        return current_cycle - self.start


class ReservationEntry:
    """ReservationEntry Class to model the entries into
    the different reserveration stations for each set of
    functional units.
    """

    def __init__(self, op_type, current_cycle):
        self.operation = op_type
        self.entry_cycle = current_cycle
        self.source_1 = None
        self.source_2 = None
        self.res_1 = None
        self.res_2 = None

    def set_source_1(self, s1):
        """Sets the source 1 when it is available

        Keyword arguments:
        s1 -- the location of s1

        Returns: None
        """
        self.source_1 = s1

    def set_source_2(self, s1):
        """Sets the source 2 when it is available

        Keyword arguments:
        s2 -- the location of s2

        Returns: None
        """
        self.source_1 = s1

    def set_res_1(self, r1):
        """Sets the resveration station 1 producing source 1

        Keyword arguments:
        r1 -- the reservation station for s1

        Returns: None
        """
        self.res_1 = r1

    def set_res_2(self, r2):
        """Sets the reservation station 2 producing source 2

        Keyword arguments:
        r2 -- the reservation station for s2

        Returns: None
        """
        self.res_2 = r2

    def get_entry_time(self):
        """Gets the time the reservation station was added

        Keyword arguments:
        None

        Returns: Int
        """
        return self.entry_cycle

    def check_readiness(self):
        """Checks if a reservation entry is ready for execution

        Keyword arguments:
        None

        Returns: Boolean
        """
        return bool(self.source_1 is not None and self.source_2 is not None)


class FunctionalUnit:
    """FunctionalUnit Class to encompass methods needed for
       Integer, Divide, Multipler, Load, Store Functional
       Units in tomsim
    """

    def __init__(self, func_id, lat):
        self.instruction_count = 0
        self.latency = lat
        self.status = FREE
        self.func_id = func_id
        self.end_cycle = None
        self.destination = None

    def __str__(self):
        return """
            Id:                {}
            Instruction Count: {}
            Latency:           {}
            Status:            {}
            End Cycle:         {}
            Destination        {}
            """.format(self.func_id,
                       self.instruction_count,
                       self.latency,
                       self.status,
                       self.end_cycle,
                       self.destination)

    def get_statistics(self):
        """Gets the statistics for the functional unit

        Keyword arguments:
        None

        Returns: Tuple of function id and instruction count
        """

        return (self.func_id, self.instruction_count)

    def get_end(self):
        """Gets the end cycle

        Keyword arguments:
        None

        Returns: Int of the end cycle
        """

        return self.end_cycle

    def get_destination(self):
        """Gets the location to which the functional unit will
        write

        Keyword arguments:
        None

        Returns: String of renamed destination
        """

        return self.destination

    def start_op(self, current_cycle):
        """Starts execution of the functional unit.  The unit is now busy

        Keyword arguments:
        current_cycle -- the cycle on which execution begins

        Returns: None
        """

        self.status = BUSY
        self.instruction_count += 1
        self.end_cycle = self.latency + current_cycle

    def end_op(self):
        """Ends the execution of the functional unit.  The unit is now free

        Keyword arguments:
        None

        Returns None
        """
        self.status = FREE

def parse_trace(trace_file):
    """Parses the trace TEXT file into an array 
    for processing during the simulation
        
    Keyword arguments:
    trace_file -- the trace on instructions to simulate     

    Returns: List 
    """
    
    instructions = []

    with open(trace_file) as instruction_trace:
        for line in instruction_trace:
            if line[0] is not '#': 
                line = line.strip()
                binary_value = bin(int(line, 16))[2:].zfill(16)
                instructions.append(binary_value)

    return instructions

def get_instruction(instructions, instruction_count):
    """Gets the next instruction and produces
    the necessary issue event

    Keyword arguments:
    instructions -- the array of instructions
    instructions_count -- the index of the next instruction 


    Return: PipeEvent  
    """

    instruction_hex = instructions[instruction_count] 
                   

       
        

def parse_config(config_file):
    """Parses the config JSON file into a dictionary
       to initialize the simulation

       Keyword arguments:
       config_file -- the path of configuration JSON file

       Returns: None
    """
    with open(config_file) as configuration:
        config_values = json.load(configuration)

    for functional_unit, config_list in config_values.items():

        unit_config = config_list[0]

        if functional_unit == 'integer':
            INT_RS_MAX = unit_config['resnumber']
            latency = unit_config['latency']

            for i in range(unit_config['number']):
                INTEGER.append(FunctionalUnit(i, latency))

        elif functional_unit == 'divider':
            DIV_RS_MAX = unit_config['resnumber']
            latency = unit_config['latency']

            for i in range(unit_config['number']):
                DIVIDER.append(FunctionalUnit(i, latency))

        elif functional_unit == 'multiplier':
            MULT_RS_MAX = unit_config['resnumber']
            latency = unit_config['latency']

            for i in range(unit_config['number']):
                MULTIPLIER.append(FunctionalUnit(i, latency))

        elif functional_unit == 'load':
            LD_RS_MAX = unit_config['resnumber']
            latency = unit_config['latency']

            for i in range(unit_config['number']):
                LOAD.append(FunctionalUnit(i, latency))

        elif functional_unit == 'store':
            ST_RS_MAX = unit_config['resnumber']
            latency = unit_config['latency']

            for i in range(unit_config['number']):
                STORE.append(FunctionalUnit(i, latency))

        else:
            print('INVALID UNIT')


def get_unit_statistics():
    """Displays the statistics for all functional
    units

    Keyword arguments:
    None

    Return: None
    """

    print('--INTEGER STATS--')
    for functional_unit in INTEGER:
        print(functional_unit)

    print('--DIVIDER STATS--')
    for functional_unit in DIVIDER:
        print(functional_unit)

    print('--MULTIPLIER STATS--')
    for functional_unit in MULTIPLIER:
        print(functional_unit)

    print('--LOAD STATS--')
    for functional_unit in LOAD:
        print(functional_unit)

    print('--STORE STATS--')
    for functional_unit in STORE:
        print(functional_unit)


def tomsim(trace_file, config_file, output_file):
    """Simulates Tomasulos on the given trace
       based on the information in the configuration
       file and outputs statistics to the output_file

       Keyword arguments:
       trace_file -- trace file of X encoded instructions
       config_file -- defines system set up
       output_file -- output json file

       Return: None
    """
    print(trace_file)
    print(config_file)
    print(output_file)

    parse_config(config_file)
    get_unit_statistics()

    instructions = parse_trace(trace_file)
    pprint(instructions)




if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: ./tomsim tracefile config.json output.json')
        exit(1)

    TRACE_FILE = sys.argv[1]
    CONFIG_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    tomsim(TRACE_FILE, CONFIG_FILE, OUTPUT_FILE)
