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
 * Tests for vs*.v instructions
 * 
 *    vss*pi.v vs3, (rs1), rs2, vm
 * 
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VSSX_V_H
#define __TEST_MACROS_VSSX_V_H

#include "test_macros_v.h"
#include "exception.h"

/*******************************************************************************
 * Functional tests without mask
 ******************************************************************************/

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSxPI_V_INTERNAL(testnum, inst, result, mem, vs3, rs2, vlen, slen, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, vs3, (vlen * ebits/8), lb, sb, 1); \
    COPY(RD_ADDR, mem, (slen * ebits/8), lb, sb, 1); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, rs2 ; \
    lw a2, 0(a2) ; \
    la a3, RD_ADDR ; \
  vsetvli a4, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v1, (a3), a2 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a1, RD_ADDR; \
    la a2, rs2 ; \
    lw a2, 0(a2) ; \
    mul a2, a2, a4 ; \
    add a2, a2, a1; \
    bne a3, a2, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    COPY(mem, RD_ADDR, (slen * ebits/8), lb, sb, 1); \
    eqm(result, mem, vlen);

/**
 * vssepi.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSEPI_V(testnum, result, mem, vs3, rs2, vlen, slen, ebits, eqm) \
  TEST_VSSxPI_V_INTERNAL(testnum, vssepi.v, result, mem, vs3, rs2, vlen, slen, ebits, vle.v, eqm)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSxPI_V_MASK_INTERNAL(testnum, inst, result, mem, vs3, rs2, vlen, slen, mask, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, vs3, (vlen * ebits/8), lb, sb, 1); \
    COPY(MASK_ADDR, mask, (vlen * ebits/8), lb, sb, 1); \
    COPY(RD_ADDR, mem, (slen * ebits/8), lb, sb, 1); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, rs2 ; \
    lw a2, 0(a2) ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
  vsetvli a5, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  inst v1, (a3), a2, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    la a1, RD_ADDR; \
    la a2, rs2 ; \
    lw a2, 0(a2) ; \
    mul a2, a2, a5 ; \
    add a2, a2, a1; \
    bne a3, a2, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    COPY(mem, RD_ADDR, (slen * ebits/8), lb, sb, 1); \
    eqm(result, mem, vlen);

/**
 * vssepi.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSEPI_V_MASK(testnum, result, mem, vs3, rs2, vlen, slen, mask, ebits, eqm) \
  TEST_VSSxPI_V_MASK_INTERNAL(testnum, vssepi.v, result, mem, vs3, rs2, vlen, slen, mask, ebits, vle.v, eqm)


/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @soff1     address offset for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSSEPI_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \


/**
 * Misaligned stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @rs2       stride
 * @ebits     element size in bits
 */
#define TEST_VSSEPI_V_MISALIGNED_STRIDE( testnum, inst, vlen, rs2, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_OFFSET, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  la a2, rs2 ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR ; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \



/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSSEPI_V_ACCESS_FAULT( testnum, inst, vlen, vs3, rs2, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  la a2, rs2 ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, vs3; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \

#endif // __TEST_MACROS_VSSX_V_H
