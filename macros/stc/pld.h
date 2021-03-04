/*
 * Copyright (c) 2020 Stream Computing Corp.
 * All rights reserved
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * Tests for pld instruction
 * 
 *    pld (rd), (rs1)
 * 
 * Authors: Bin Jiang
 */
#ifndef __TEST_MACROS_PLD_COMMON_H
#define __TEST_MACROS_PLD_COMMON_H

#include "test_macros.h"
#include "test_macros_v.h"
#include "exception.h"

// set mte csr
#define set_mte_csr(height, width, stride, coremap) 	\
  li t0, ((width << 16) | (height&0xffff));	\
  csrw mte_shape, t0; 			\
  li t0, ((stride*2) & 0xffff);		\
  csrw mte_stride_llb, t0;		\
  li t0, (coremap & 0xffff); 		\
  csrw mte_coremap, t0;			\

/*******************************************************************************
 * pld Functional tests
 ******************************************************************************/

/**
 * pld Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 * @setcsr    inst to set csr
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 */
#define TEST_PLD_INTERNAL(testnum, inst, verify, dest, src, height, width, \
                              stride, coremap, setcsr, ebits) \
    li TESTNUM, testnum; \
    li a1, width*height*(ebits/8); \
    la a0, dest; \
    add a1, a0, a1;  \
100: \
    bge a0, a1, 101f; \
    sb zero, (a0); \
    addi a0, a0, 1; \
    j 100b; \
101: \
    csrr a0, tid; \
    andi a0, a0, 0x7; \
    li a1, 1; \
    sll a0, a1, a0; \
    andi a0, a0, coremap; \
    bnez a0, 102f; \
    PERF_NOP() \
    sync; \
    VV_SB_CHECK_EQ(test_ ## testnum ## _zero, dest, width * height*(ebits/8)); \
    j 103f; \
102: \
    setcsr(height, width, stride, coremap); \
    PERF_BEGIN() \
    la a0, src; \
    la a1, dest; \
  inst (a1), (a0); \
    PERF_END8(width ## _ ## height) \
    fence.i; \
    sync;	\
    VV_SB_CHECK_EQ(verify, dest, width * height*(ebits/8)); \
103: \
    .pushsection .data; \
test_ ## testnum ## _zero: \
    .fill width * height, (ebits/8), 0; \
    .popsection

/**
 * pld HF Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_PLD_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_INTERNAL(testnum, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

/**
 * multi-pld HF Functional tests
 * run times pld insts to transfer height*width*times data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @times     times to call inst
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_MULTI_PLD_HF(testnum, inst, verify, dest, src, height, width, times, stride, coremap) \
    li TESTNUM, testnum; \
    li a1, width*height*2*times; \
    la a0, dest; \
    add a1, a0, a1;  \
200: \
    bge a0, a1, 201f; \
    sw zero, (a0); \
    addi a0, a0, 4; \
    j 200b; \
201: \
    la a0, src; \
    la a1, dest; \
    li a2, width*height*2; \
    li a3, times; \
202: \
    set_mte_csr(height, width, stride, coremap); \
  inst (a1), (a0); \
    add a0, a0, a2; \
    add a1, a1, a2; \
    addi a3, a3, -1; \
    bnez a3, 202b; \
    sync;	\
    VV_SB_CHECK_EQ(verify, dest, width * height * (16/8) *times);

/*******************************************************************************
 * pld exception tests
 ******************************************************************************/

/**
 * pld exception base functon
 *
 * @testnum   test case number
 * @exception exception number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 * @setcsr    inst to set csr
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 */
#define TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, exception, inst, verify, dest, src, height, width, \
                              stride, coremap, setcsr, ebits) \
    li TESTNUM, testnum; \
test_ ## testnum: \
    TEST_EXCEPTION(exception, test_ ## testnum ## _end); \
    setcsr(height, width, stride, coremap); \
    la a0, src; \
    la a1, dest; \
  inst (a1), (a0); \
    j fail; \
test_ ## testnum ## _end: \
    sync;      \

/**
 * pld HF invalid start address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_PLD_INVALID_L1_START_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_START, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

#define TEST_PLD_INVALID_LLB_START_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ILLEGAL_ENCODEING, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

/**
 * pld HF invalid L1 end address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_PLD_INVALID_L1_END_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_END_L1, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

/**
 * pld HF invalid LLB end address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_PLD_INVALID_LLB_END_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_END_LLB, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

/**
 * pld HF invalid parameter tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store  result
 * @src       start addr to load source
 * @height    LLB matrix height
 * @width     LLB matrix width
 * @stride    LLB matrix stride
 * @coremap   core map to recv data
 */
#define TEST_PLD_INVALID_PARAM_HF(testnum, inst, verify, dest, src, height, width, stride, coremap) \
  TEST_PLD_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_INVALID_PARAM, inst, verify, dest, src, height, width,stride, coremap, set_mte_csr, 16);

#endif // __TEST_MACROS_PLD_COMMON_H
