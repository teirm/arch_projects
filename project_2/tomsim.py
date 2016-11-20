#!/usr/bin/python
"""
Project: tomsim simulator
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    19 November 2016
"""

import sys
import json

# DEFINES
BUSY = 1
FREE = 0


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


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: ./tomsim tracefile config.json output.json')
        exit(1)

    TRACE_FILE = sys.argv[1]
    CONFIG_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]

    tomsim(TRACE_FILE, CONFIG_FILE, OUTPUT_FILE)
