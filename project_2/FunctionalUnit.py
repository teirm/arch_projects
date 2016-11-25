"""
Project: tomsim simulator
Module: FunctionalUnit
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    19 November 2016
"""

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

    def get_latency(self):
        """Gets the latency of the functional unit

        Keyword arguments:
        None

        Return: Int
        """
        return self.latency

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
        return self.status

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
