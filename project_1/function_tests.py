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
   

def test_branch_positive_taken():
    """Tests the branch positive instruction
       when the branch is taken 
    """
    init()
    Rd = '010'
    cond = Bits(int=123, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    liz(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 40   
    return_value = branch_positive(data_fields, program_counter) 

    assert expected_value == return_value 


def test_branch_positive_not_taken():
    """Tests the branch positive instruction
       when the branch is not taken 
    """
    init()
    Rd = '011'
    cond = Bits(int=-65, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 1   
    return_value = branch_positive(data_fields, program_counter) 

    assert expected_value == return_value 


def test_branch_negative_taken():     
    """Tests the branch negative instruction
       when the branch is taken 
    """
    init()
    Rd = '100'
    cond = Bits(int=-3, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 40   
    return_value = branch_negative(data_fields, program_counter) 

    assert expected_value == return_value 

     
def test_branch_negative_not_taken():     
    """Tests the branch negative instruction
       when the branch is not taken 
    """
    init()
    Rd = '100'
    cond = Bits(int=+3, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 1   
    return_value = branch_negative(data_fields, program_counter) 

    assert expected_value == return_value 
          

def test_branch_not_zero_positive():
    """Tests the branch neq 0 instruction
       when the branch is taken
    """
    init()
    Rd = '101'
    cond = Bits(int=30, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 40   
    return_value = branch_nzero(data_fields, program_counter) 

    assert expected_value == return_value 


def test_branch_not_zero_negative():
    """Tests the branch neq 0 instruction
       when the branch is taken
    """
    init()
    Rd = '101'
    cond = Bits(int=-30, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 40   
    return_value = branch_nzero(data_fields, program_counter) 

    assert expected_value == return_value 

      
def test_branch_not_zero_not_taken():
    """Tests the branch neq 0 instruction
       when the branch is taken
    """
    init()
    Rd = '101'
    cond = Bits(int=0, length=8).bin 
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=20, length=8).bin
    data_fields = ''.join([Rd, Imm8])  
    
    expected_value = program_counter + 1   
    return_value = branch_nzero(data_fields, program_counter) 

    assert expected_value == return_value 


