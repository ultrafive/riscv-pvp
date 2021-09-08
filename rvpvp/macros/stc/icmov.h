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
 * Tests for icmov instruction
 * 
 *    icmov (rd), (rs1), rs2
 * 
 * Authors: Bin Jiang
 */
#ifndef __TEST_MACROS_ICMOV_COMMON_H
#define __TEST_MACROS_ICMOV_COMMON_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

// L1 address of RS1
#define ICMOV_RS1_ADDR  0xc0000000

// set mte csr
#define set_mte_csr(chipid, coreid) 			\
  li t0, (((chipid&0xf) << 16) | (coreid&0x3f));	\
  csrw mte_icdest, t0; 					\

/*******************************************************************************
 * icmov Functional tests
 ******************************************************************************/

/**
 * icmov Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 * @setcsr    inst to set csr
 */
#define TEST_ICMOV_INTERNAL(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core, setcsr) \
    li TESTNUM, testnum; \
    csrr a0, tid; \
    andi a0, a0, 0x7; \
    li a1, src_core; \
    beq a0, a1, 100f; \
    li a1, dest_core; \
    beq a0, a1, 101f; \
    PERF_NOP() \
    sync; \
    j 102f; \
100: \
    COPY(ICMOV_RS1_ADDR, src, len, lb, sb, 1); \
    setcsr(dest_chip, dest_core); \
    PERF_BEGIN() \
    la a0, ICMOV_RS1_ADDR; \
    la a1, dest; \
    li a3, len; \
  inst (a1), (a0), a3; \
    PERF_END8(testnum) \
    sync;	\
    j 102f; \
101: \
    PERF_NOP() \
    sync;	\
    VV_CHECK_EQ_INT8(verify, dest, len); \
102: \

/**
 * icmov HF Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 */
#define TEST_ICMOV_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core) \
  TEST_ICMOV_INTERNAL(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core, set_mte_csr);

/**
 * multi-icmov HF Functional tests
 * run times icmov insts to transfer len*times data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 * @times     times to do inst
 */
#define TEST_MULTI_ICMOV_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core, times) \
    li TESTNUM, testnum; \
    csrr a0, tid; \
    andi a0, a0, 0x7; \
    li a1, src_core; \
    beq a0, a1, 100f; \
    li a1, dest_core; \
    beq a0, a1, 101f; \
    sync; \
    j 102f; \
100: \
    COPY(ICMOV_RS1_ADDR, src, len*times, lb, sb, 1); \
    la a0, ICMOV_RS1_ADDR; \
    la a1, dest; \
    li a2, len; \
    li a3, times; \
    set_mte_csr(dest_chip, dest_core); \
103: \
  inst (a1), (a0), a2; \
    add a0, a0, a2; \
    add a1, a1, a2; \
    addi a3, a3, -1; \
    bnez a3, 103b; \
    sync; \
    j 102f; \
101: \
    sync;	\
    VV_CHECK_EQ_INT8(verify, dest, len *times); \
102: \

/**
 * icmov to neighbor(core->core+1) in chip 0 HF Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 */
#define TEST_ICMOV_TO_NEIGHBOR_HF(testnum, inst, verify, dest, src, len) \
    li TESTNUM, testnum; \
    COPY(ICMOV_RS1_ADDR, src, len, lb, sb, 1); \
    csrr a0, tid; \
    andi a0, a0, 0x7; \
    addi a1, a0, 1; \
    andi a1, a1, 0x7; \
    csrw mte_icdest, a1; \
    la a0, ICMOV_RS1_ADDR; \
    la a1, dest; \
    li a3, len; \
  inst (a1), (a0), a3; \
    sync;	\
    VV_CHECK_EQ_INT8(verify, dest, len); \


/*******************************************************************************
 * icmov exception tests
 ******************************************************************************/

/**
 * icmov exception base functon
 *
 * @testnum   test case number
 * @exception exception number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 * @setcsr    inst to set csr
 */
#define TEST_ICMOV_WITH_EXCEPTION_INTERNAL(testnum, exception, inst, verify, dest, src, len, src_core, dest_chip, dest_core, setcsr) \
    li TESTNUM, testnum; \
test_ ## testnum: \
    TEST_EXCEPTION(exception, test_ ## testnum ## _end); \
    csrr a0, tid; \
    andi a0, a0, 0x7; \
    li a1, src_core; \
    beq a0, a1, 100f; \
    li a1, dest_core; \
    beq a0, a1, 101f; \
    sync; \
    j 102f; \
100: \
    setcsr(dest_chip, dest_core); \
    la a0, src; \
    la a1, dest; \
    li a3, len; \
  inst (a1), (a0), a3; \
test_ ## testnum ## _end: \
101: \
    sync;	\
102: \


/**
 * icmov HF invalid rd start address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 */
#define TEST_ICMOV_INVALID_RD_START_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core) \
  TEST_ICMOV_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_START_ICMOV, inst, verify, dest, src, len, src_core, dest_chip, dest_core, set_mte_csr);

/**
 * icmov HF invalid rs1 start address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 */
#define TEST_ICMOV_INVALID_RS1_START_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core) \
  TEST_ICMOV_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_START, inst, verify, dest, src, len, src_core, dest_chip, dest_core, set_mte_csr);

/**
 * icmov HF invalid L1 end address tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 */
#define TEST_ICMOV_INVALID_L1_END_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core) \
  TEST_ICMOV_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_ACCESS_END_L1, inst, verify, dest, src, len, src_core, dest_chip, dest_core, set_mte_csr);

/**
 * icmov HF invalid parameter tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @verify    start addr to verify result
 * @dest      start addr to store result
 * @src       start addr to load source
 * @len       length of data
 * @src_core  source core ID
 * @dest_chip dest chip ID
 * @dest_core dest core ID
 */
#define TEST_ICMOV_INVALID_PARAM_HF(testnum, inst, verify, dest, src, len, src_core, dest_chip, dest_core) \
  TEST_ICMOV_WITH_EXCEPTION_INTERNAL(testnum, CAUSE_TCP_INVALID_PARAM, inst, verify, dest, src, len, src_core, dest_chip, dest_core, set_mte_csr);

#endif // __TEST_MACROS_ICMOV_COMMON_H
