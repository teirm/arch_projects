#!/usr/bin/python
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

#DEFINES

WORD_SIZE = 16


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

    Imm8 = Bits(uint=32, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    expected_value = 4 
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

    Imm8 = Bits(uint=32, length=8).bin
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

    expected_value = int(40 / 16)
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

    expected_value = int(40 / WORD_SIZE)
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

    expected_value = int(40 / WORD_SIZE)
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


def test_branch_zero_taken():
    init()
    Rd = '101'
    cond = Bits(int=0, length=8).bin
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=60, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    expected_value = int(120 / WORD_SIZE)
    return_value = branch_zero(data_fields, program_counter)

    assert expected_value == return_value


def test_branch_zero_not_taken_positive():
    """Test branch zero not taken with a
       positive number.
    """
    init()
    Rd = '101'
    cond = Bits(int=3, length=8).bin
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=60, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    expected_value = program_counter + 1
    return_value = branch_zero(data_fields, program_counter)

    assert expected_value == return_value


def test_branch_zero_not_taken_negative():
    """Test branch zero not taken with a
       negative number.
    """
    init()
    Rd = '101'
    cond = Bits(int=-32, length=8).bin
    program_counter = 10

    data_fields = ''.join([Rd, cond])
    lis(data_fields)

    Imm8 = Bits(uint=60, length=8).bin
    data_fields = ''.join([Rd, Imm8])

    expected_value = program_counter + 1
    return_value = branch_zero(data_fields, program_counter)

    assert expected_value == return_value


def test_jump_register_negative():
    """Test the jump register function by jumping
       backward.
    """
    init()
    Rd = '110'
    Rs = '101'
    Rt = '111'
    program_counter = 10

    jump_value = Bits(int=-48, length=8).bin
    load_data_fields = ''.join([Rs, jump_value])
    lis(load_data_fields)

    data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -3
    return_value = jump_register(data_fields, program_counter)

    assert expected_value == return_value


def test_jump_register_positive():
    """Test the jump register function by jumping
       forward.
    """
    init()
    Rd = '110'
    Rs = '101'
    Rt = '111'
    program_counter = 10

    jump_value = Bits(int=48, length=8).bin
    load_data_fields = ''.join([Rs, jump_value])
    lis(load_data_fields)

    data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 3
    return_value = jump_register(data_fields, program_counter)

    assert expected_value == return_value


def test_jump_and_link():
    """Test the jump and link instruction."""
    init()
    Rd = '110'
    Rs = '101'
    Rt = '111'
    program_counter = 10

#   Load only an 8 bit value because that is what liz does
    jump_value = Bits(uint=160, length=8).bin
    load_data_fields = ''.join([Rs, jump_value])
    liz(load_data_fields)

    data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 10 
    return_value = jump_and_link_register(data_fields, program_counter)

    assert expected_value == return_value
    assert Bits(bin=REGISTER_FILE['r6']).int == 11 * 16


def test_jump_immediate():
    """Test jump_immediate
       NOTE: Shift will rotate large numbers to
       a smaller value by rotating off the 1."""
    init()
    imm11 = Bits(uint=231, length=11).bin
    program_counter = 23
    pc_bits = Bits(int=23, length=16)

    expected_value = int(462 / 16)
    return_value = jump_immediate(imm11, program_counter)

    assert expected_value == return_value


def test_add_instruction_positives():
    """Tests the add instruction with two
       positive numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    liz(left_data_fields)
    liz(right_data_fields)

    add_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 156
    return_value = add_instruction(add_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_add_intstruction_negatives():
    """Tests the add instruction with two
       negative numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=-73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    add_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -156
    return_value = add_instruction(add_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_add_intstruction_mixed():
    """Tests the add instruction with two
       negative numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    add_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -10
    return_value = add_instruction(add_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_sub_intruction_pos():
    """Tests the sub instruction with two
       positive numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    sub_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 10
    return_value = sub_instruction(sub_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_sub_intruction_neg():
    """Tests the sub instruction with two
       positive numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=-73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    sub_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -10
    return_value = sub_instruction(sub_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_sub_intruction_mixed():
    """Tests the sub instruction with two
       positive numbers.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    sub_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -156
    return_value = sub_instruction(sub_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_and_instruction():
    """Tests the  and instruction with a positive
       and a negative value.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    and_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = (Bits(bin=right_operand) & Bits(bin=left_operand)).bin
    return_value = and_instruction(and_data_fields)


def test_nor_instruction():
    """Tests the nor instruction with a positive
       and a negative value.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=73, length=8).bin
    left_operand = Bits(int=-83, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    nor_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = (~(Bits(bin=right_operand) |
                        Bits(bin=left_operand))).bin.zfill(16)
    return_value = nor_instruction(nor_data_fields)

    assert expected_value == return_value


def test_div_instruction():
    """Tests the div instruction with a positive and a
       negative value.
    """
    Rd = '101'
    Rs = '011'
    Rt = '001'

    right_operand = Bits(int=11, length=8).bin
    left_operand = Bits(int=-121, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    div_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -11

    return_value = div_instruction(div_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_mult_instruction_small():
    """Tests the mul instruction with a positive and a
       negative small values
    """
    init()
    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=4, length=8).bin
    left_operand = Bits(int=-2, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    mul_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = -8

    return_value = mul_instruction(mul_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_mult_instruction_large():
    """Tests the mul instruction with a positive and a
       negative large values
    """
    init()
    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=125, length=8).bin
    left_operand = Bits(int=124, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    mul_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 15500

    return_value = mul_instruction(mul_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_mod_instruction():
    """Tests the modulus instruction with a two
       positive values.
    """
    init()
    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=7, length=8).bin
    left_operand = Bits(int=3, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    mod_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 1
    return_value = mod_instruction(mod_data_fields)


def test_exp_instruction():
    """Tests the exponentiation function with
       two positive numbers.
    """
    init()
    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=7, length=8).bin
    left_operand = Bits(int=3, length=8).bin

    left_data_fields = ''.join([Rs, left_operand])
    right_data_fields = ''.join([Rt, right_operand])

    lis(left_data_fields)
    lis(right_data_fields)

    exp_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = 2187
    return_value = exp_instruction(exp_data_fields)

    assert expected_value == Bits(bin=return_value).int


def test_lw_instruction():
    """Tests the load word function"""
    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=16, length=8).bin
    load_register_fields = ''.join([Rs, right_operand])
    lis(load_register_fields)

    DATA_MEMORY[right_operand.zfill(16)] = 16 
    load_data_fields = ''.join([Rd, Rs, Rt])

    expected_value = Bits(int=DATA_MEMORY[right_operand.zfill(16)], length=16).bin
    return_value = load_word(load_data_fields)

    assert expected_value == return_value


def test_sw_instruction():
    """Tests the store word instruction"""

    Rd = '101'
    Rs = '001'
    Rt = '011'

    right_operand = Bits(int=16, length=8).bin
    load_register_fields = ''.join([Rt, right_operand])
    lis(load_register_fields)

    left_operand = Bits(int=32, length=16).bin
    load_register_fields = ''.join([Rs, left_operand])
    lis(load_register_fields)

    store_word_fields = ''.join([Rd, Rs, Rt])

    expected_value = 16
    return_value = store_word(store_word_fields)

    assert expected_value == return_value 
