#!/usr/bin/python

"""
Project: xsim simulator testing
Course: CS2410
Author: Cyrus Ramavarapu
Date: 23 October 2016
"""
import pytest
from xsim import *


from bitstring import Bits


def init():
    config_file = 'configs/config_1.json'

    statistics_dict = init_statistics_dict()
    latency_dict = configure_latency(config_file)
    init_register_file()
    program_counter = 0


def test_lis_positive():
    """Tests the load immediate with sign
       extension with a positive value.
    """
    init()
    Rd = '010'
    Imm8 = Bits(int=101, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    return_value = Bits(bin=lis(data_fields)).int

    assert 101 == return_value


def test_lis_negative():
    """Tests the load immediate with sign
       extension with a negative value.
    """
    init()
    Rd = '010'
    Imm8 = Bits(int=-101, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    return_value = Bits(bin=lis(data_fields)).int

    assert -101 == return_value


def test_lis_zero():
    """Tests the load immediate with sign
       extension with a negative value.
    """
    init()
    Rd = '010'
    Imm8 = Bits(int=0, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    return_value = Bits(bin=lis(data_fields)).int

    assert 0 == return_value
    
    
