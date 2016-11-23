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

# OPCODE MAPPING

OPCODE_MAP = {'00000': 'add',
              '00001': 'sub',
              '00010': 'and',
              '00011': 'nor',
              '00100': 'div',
              '00101': 'mul',
              '00110': 'mod',
              '00111': 'exp',
              '01000': 'lw',
              '01001': 'sw',
              '10001': 'lis',
              '10000': 'liz',
              '10010': 'lui',
              '01101': 'halt',
              '01110': 'put'}

# Need to store latencies some where


class PipeEvent:
    """Event entry for tomsim to model ISSUE,
    READ_OPERAND, EXECUTE, and WRITE_REGISTER
    """

    def __init__(self, event_type, instr, current_cycle, latency):
        self.event = event_type
        self.instruction = instr
        self.start = current_cycle
        self.end = current_cycle + latency
        self.dest = None
        self.source_1 = None
        self.source_2 = None
        self.location = None
        self.position = None

    def __str__(self):
        return """Event:       {}
           Instruction: {}
           Destination: {}
           Source 1:    {}
           Source 2:    {}
           Start:       {}
           End:         {}
           Location:    {}
           Position:    {}
           """.format(self.event,
                      self.instruction,
                      self.dest,
                      self.source_1,
                      self.source_2,
                      self.start,
                      self.end,
                      self.location,
                      self.position)

    def get_instruction(self):
        """Returns the instruction type of the event

        Keyword arguments:
        None

        Returns: String
        """
        return self.instruction

    def set_sources(self, s1, s2):
        """Sets the sources for the event

        Keyword arguments:
        s1 -- source operand 1 or FU producing
        s2 -- source operand 2 or FU producing

        Returns: None
        """
        self.source_1 = s1
        self.source_2 = s2

    def set_resv_info(self, res_name, res_pos):
        """Sets the reservation station for the event
        and its location in the reservation station

        Keyword arguments:
        res_name -- name of the reservation station (INT_RS, DIV_RS...)
        res_pos -- position in the reservation station

        Returns: None
        """
        self.location = res_name
        self.position = res_pos

    def set_destination(self, dest):
        """Sets the destination for the event

        Keyword arguments:
        dest -- destination FU producing

        Returns: None
        """
        self.dest = dest

    def get_destination(self):
        """Gets the FU for the event

        Keyword arguments:
        None

        Returns: None
        """
        return self.dest

    def update_event(self, new_event):
        """Updates the event as it moves through
        the event queue

        Keyword arguments:
        new_event -- the new event for this object
        new_start -- new start time
        new_end -- new end time

        Returns: None
        """
        self.event = new_event

    def update_start(self, new_start):
        """Updates the start time of an event

        Keyword arguments:
        new_start -- new start time

        Returns: None
        """
        self.start = new_start

    def update_end(self, new_end):
        """Updates the end time of an event

        Keyword arguments:
        new_end -- new end time

        Returns: None
        """
        self.end == new_end

    def get_event(self):
        """Returns the event type

        Keyword arguments:
        None

        Returns: String
        """
        return self.event

    def get_sources(self):
        """Returns the sources for the event

        Keyword arguments:
        None

        Returns: Tuple of sources
        """
        return (self.source_1, self.source_2)

    def get_age(self, current_cycle):
        """Computes the age of the event based
        on its start cycle and the current cycle

        Keyword arguments:
        current_cycle -- the current cycle of execution

        Returns: Int
        """
        return current_cycle - self.start

    def get_resv_info(self):
        """Returns the reservation station information
        to the caller for this PipeEvent

        Keyword arguments:
        None

        Returns: Tuple of (resv_name, resv_pos)
        """
        return (self.location, self.position)

    def get_end(self):
        """Returns the time at which the event
        is supposed to end.

        Keyword arguments:
        None

        Returns: Int
        """
        return self.end


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

    def set_status(self, status):
        """Sets the status of a functional unit

        Keyword arguments:
        status -- the status to set a functional unit to
                  either BUSY or FREE

        Returns
        None
        """
        self.status = status

    def get_status(self):
        """Gets the status of a functional unit

        Keyword arguments:
        None

        Return: Int FREE (0) or BUSY (1)
        """

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
    the type and source operands

    Keyword arguments:
    instructions -- the array of instructions
    instructions_count -- the index of the next instruction


    Return: Tuple
    """

    i_type = ['liz', 'lis', 'lui']

    next_instruction = instructions[instruction_count]
    opcode = next_instruction[0:5]

    instruction_type = OPCODE_MAP[opcode]

    if instruction_type in i_type:
        dest = ''.join(['r', str(int(next_instruction[5:8], 2))])
        # USE 'IMM8' to recoginize that the source operand
        # is immediately available
        source_1 = 'IMM8'
        source_2 = None
    elif instruction_type is 'put':
        dest = None
        source_1 = ''.join(['r', str(int(next_instruction[8:11], 2))])
        source_2 = None
    elif instruction_type is 'halt':
        dest = None
        source_1 = None
        source_2 = None
    else:
        dest = ''.join(['r', str(int(next_instruction[5:8], 2))])
        source_1 = ''.join(['r', str(int(next_instruction[8:11], 2))])
        source_2 = ''.join(['r', str(int(next_instruction[11:14], 2))])

    return (instruction_type, dest, source_1, source_2)


def parse_config(config_file):
    """Parses the config JSON file into a dictionary
       to initialize the simulation

       Keyword arguments:
       config_file -- the path of configuration JSON file

       Returns: None
    """

    global INT_RS_MAX
    global DIV_RS_MAX
    global MULT_RS_MAX
    global LD_RS_MAX
    global ST_RS_MAX

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


def get_resv_station(op_name):
    """Checks if a reservation station is available
    and if it is fills in reservation station with the
    given operation

    Keyword arguments:
    op_name -- the name of the operation

    Returns: Tuple of RS type and Int of position in RS if successful otherwise None, -1
    """

    int_operations = [
        'add',
        'sub',
        'nor',
        'and',
        'lis',
        'liz',
        'lui',
        'put',
        'halt']
    div_operations = ['div', 'exp', 'mod']

    if op_name in int_operations:
        if len(INT_RS) < INT_RS_MAX:
            print('INT RS AVAILABLE FOR {}'.format(op_name))
            ret_val = ('INT', len(INT_RS))
            INT_RS.append(BUSY)
        else:
            print('INT RS NOT AVAILABLE FOR {}'.format(op_name))
            ret_val = (None, -1)
    elif op_name in div_operations:
        if len(DIV_RS) < DIV_RS_MAX:
            print('DIV RS AVAILABLE FOR {}'.format(op_name))
            ret_val = ('DIV', len(DIV_RS))
            DIV_RS.append(BUSY)
        else:
            print('DIV RS NOT AVAILABLE FOR {}'.format(op_name))
            ret_val = (None, -1)
    elif op_name is 'mul':
        if len(MULT_RS) < MULT_RS_MAX:
            print('MULT RS AVAILABLE FOR {}'.format(op_name))
            ret_val = ('MULT', len(MULTIPLIER))
            MULT_RS.append(BUSY)
        else:
            print('MULT RS NOT AVAILABLE FOR {}'.format(op_name))
            ret_val = (None, -1)
    elif op_name is 'lw':
        if len(LD_RS) < LD_RS_MAX:
            print('LD RS AVAILABLE FOR {}'.format(op_name))
            LD_RS.append(BUSY)
            ret_val = ('LD', len(LOAD))
        else:
            print('LD RS NOT AVAILABLE FOR {}'.format(op_name))
            ret_val = (None, -1)
    else:
        if len(ST_RS) < ST_RS_MAX:
            print('ST RS AVAILABLE FOR {}'.format(op_name))
            ST_RS.append(BUSY)
            ret_val = ('ST', len(STORE))
        else:
            print('ST RS NOT AVAILABLE FOR {}'.format(op_name))
            ret_val = (None, -1)

    return ret_val

# EVENT HANDLERS


def write_op_handler(current_cycle):
    """Handles WRITE_OPERAND events in the event queue.
    If an event is found that can be processed on the
    current clock cycle it will set the RS_STATUS
    renamed register to True (1) and make the FU free
    (NOT BUSY).  The event is then removed from the
    EVENT QUEUE.

    Keyword arguments:
    current_cycle -- the current cycle the simulation is
                     processing

    Returns: Int indicating the number of events found
             and processed.
    """

    events_processed = 0
    queue_position = 0

    for event in EVENT_QUEUE:
        if event.get_end() == current_cycle and event.get_event() == 'WO':
            event_name = event.get_event()
            fu_destination = event.get_dest()
            (location, position) = event.get_resv_info()
            # Update REG_STATUS
            # free FU for event_name and RS
            EVENT_QUEUE.remove(queue_position)
            events_processed += 1

        queue_position += 1

    return events_processed


def exec_handler(current_cycle):
    """Handles EXECUTE events in the event queue.
    If an event is found that can be processed on
    the current clock cycle it will upgrade the
    event to the WRITE_OPERAND EVENT and mark
    update the start and end times.

    Keyword arguments:
    current_cycle -- the current cycle the simulation
                     is processing

    Returns: Int indiciatng the number of events found
             and processed.
    """

    events_processed = 0

    for event in EVENT_QUEUE:
        if event.get_end() == current_cycle and event.get_event() == 'EXEC':
            event.update_event('WO', current_cycle, current_cycle + 1)
            event.update_start(current_cycle)
            event.update_end(current_cycle + 1)

            events_processed += 1

    return events_processed


def check_sources(s1, s2):
    """Checks the status of the renamed registers
    to determine if a queued event can proceed
    from RO to EXEC with the necessary sources

    Keyword arguments:
    s1 -- source operand 1
    s2 -- source operand 2

    Return: Tuple with (s1 status, s2 status)
    """
    s1_status = RES_STATUS[s1]
    s2_status = RES_STATUS[s2]

    return (s1_status, s2_status)


def find_func_unit(instr):
    """Finds an available functional unit for
    the ready instruction.

    Keyword argument:
    instr -- the type of instruction being run

    Return: (Int, Int) indicating position of FU marked busy
            and its latency. (-1,-1) if none found
    """

    int_operations = [
        'add',
        'sub',
        'nor',
        'and',
        'lis',
        'liz',
        'lui',
        'put',
        'halt']
    div_operations = ['div', 'exp', 'mod']

    fu_position = 0

    if instr in int_operations:
        for int_fu in INTEGER:
            if int_fu.get_status() == FREE:
                int_fu.set_status(BUSY)
                return fu_position

            fu_position += 1
    elif instr in div_operations:
        for div_fu in DIVIDER:
            if div_fu.get_status() == FREE:
                div_fu.set_status(BUSY)
                return fu_position

        fu_position += 1
    elif instr is 'mul':
        for mul_fu in MULTIPLIER:
            if mul_fu.get_status() == FREE:
                mul_fu.set_status(BUSY)
                return fu_position

        fu_position += 1

    elif instr is 'lw':
        for ld_fu in LOAD:
            if ld_fu.get_status() == FREE:
                ld_fu.set_status(BUSY)
                return fu_position

        fu_position += 1

    else:
        for sw_fu in STORE:
            if sw_fu.get_status() == FREE:
                sw_fu.set_status(BUSY)
                return fu_position

        fu_position += 1

    return -1


def read_op_handler(current_cycle):
    """Handles READ OPERAND events in the event queue.
       If a read operand event is found, the necessary
       sources are checked for availability.  If both
       are already available, a functional unit is
       checked for availablity and assigned if possible.
       If sources are unavailable or FU not available,
       event is updated as RO with only the end cycle
       updated.

    Keyword arguments:
    current_cycle -- the current cycle the simulation is
                     processing

    Returns: Int indiciatng the number of events found
             and processed.
    """

    for event in EVENT_QUEUE:
        if event.get_event() == 'RO':
            # NEED TO FIND OLDEST FOR A GIVEN FU
            if event.get_end() == current_cycle:
                (s1, s2) = event.get_sources()
                (s1_status, s2_status) = check_sources(s1, s2)
                if (s1_status, s2_status) == (1, 1):
                    pos = find_func_unit(event.get_instruction())
                    event.update_event('EXEC')
                    event.update_start(current_cycle)
                    # MUST GET LATENCY OF FU
                    event.update_end(current_cycle + 1)
                else:
                    event.update_end(current_cycle + 1)


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
    halt_sig = False
    instruction_count = 0
    clock_cycle = 0

    parse_config(config_file)

    instructions = parse_trace(trace_file)
#    print(instructions)

    while not halt_sig:

        # Only if pipeline is NOT STALLED
        (name, dest, s1, s2) = get_instruction(instructions, instruction_count)
        (res_name, res_pos) = get_resv_station(name)
        instruction_count += 1

        # NEED FUNCTION TO HANDLE WRITE_OPS
        # NEED FUNCTION TO HANDLE EXECUTES
        # NEED FUNCTION TO HANDLE READ_OPS

        if res_name is not None:
            new_event = PipeEvent('READ_OPERAND', name, clock_cycle, 1)
            new_event.set_destination(dest)
            new_event.set_sources(s1, s2)
            new_event.set_resv_info(res_name, res_pos)

            EVENT_QUEUE.append(new_event)
        else:
            print('Stalling the Pipe')

        if name is 'halt':
            print('HALT RECEIVED')
            halt_sig = True

        clock_cycle += 1

    for event in EVENT_QUEUE:
        print("-------------------------------")
        print(event)
        print("-------------------------------")


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: ./tomsim tracefile config.json output.json')
        exit(1)

    TRACE_FILE = sys.argv[1]
    CONFIG_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    tomsim(TRACE_FILE, CONFIG_FILE, OUTPUT_FILE)
