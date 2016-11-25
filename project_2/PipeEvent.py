"""
Project: tomsim simulator
Module: PipeEvent
Course:  CS2410
Author:  Cyrus Ramavarapu
Date:    19 November 2016
"""


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
        self.source_1_status = 0
        self.source_2 = None
        self.source_2_status = 0
        self.location = None
        self.position = None
        self.func_unit = None
        self.func_id = None

    def __str__(self):
        return """Event:       {}
           Instruction: {}
           Destination: {}
           Source 1:    {}
           Source 2:    {}
           Source 1 Status: {}
           Source 2 Status: {}
           Start:       {}
           End:         {}
           Location:    {}
           Position:    {}
           """.format(self.event,
                      self.instruction,
                      self.dest,
                      self.source_1,
                      self.source_2,
                      self.source_1_status,
                      self.source_2_status,
                      self.start,
                      self.end,
                      self.location,
                      self.position)

    def set_fu_info(self, fu_id):
        """Sets the functional unit information

        Keyword arguments:
        fu_name -- name of the functional unit

        fu_id -- id of the functional unit

        Returns: None
        """
        self.func_id = fu_id

    def get_fu_info(self):
        """Gets the functional unit information

        Keyword arguments:
        None

        Returns: Tuple
        """
        return (self.location, self.func_id)

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

    def set_source_1_status(self, s1_status):
        """Sets the stats for source 1

        Keyword arguments:
        s1_status -- the status of s1

        Return: None
        """
        self.source_1_status = s1_status

    def set_source_2_status(self, s2_status):
        """Sets the stats for source 2

        Keyword arguments:
        s2_status -- the status of s2

        Return: None
        """
        self.source_2_status = s2_status

    def get_source_statuses(self):
        """Gets the statuses of source 1 and source 2

        Keyword argument:
        None

        Return: Tuple
        """
        return (self.source_1_status, self.source_2_status)

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
        self.end = new_end

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
