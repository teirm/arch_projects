"""
Project: tomsim simulator
Module: Reservation Entry
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    19 November 2016
"""


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
