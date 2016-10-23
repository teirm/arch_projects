#/usr/bin/python

"""
Project: xsim simulator testing
Course: CS2410
Author: Cyrus Ramavarapu
Date: 23 October 2016
"""
import sys
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
    
def test_lui_positive():
    """Tests the load unsigned immediate
       extension with a positive value.
    """
    init()
    Rd = '000'
    Imm8 = Bits(uint=231, length=8).bin
    data_fields = ''.join([Rd, Imm8])
    
    lower_bits = REGISTER_FILE['r0'][8:16]    
    expected_value = Bits(bin=''.join([Imm8, lower_bits])).int  
    return_value = Bits(bin=lui(data_fields)).int
   
    print(return_value, file=sys.stderr) 
    
    assert expected_value == return_value

def test_liz_positive():
    """Tests the load immediate zero
       extended.
    """
    init()
    Rd = '001'
    Imm8 = Bits(uint=216, length=8).bin
    data_fields = ''.join([Rd, Imm8])
    
    expected_value = Imm8.zfill(16)
    return_value = liz(data_fields)
    
    assert expected_value == return_value  
   
      
