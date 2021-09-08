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
 *    vsx*.v vs3, (rs1), vs2, vm
 * 
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VSXX_V_H
#define __TEST_MACROS_VSXX_V_H

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
 * @mem       start addr for data before store
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSXx_V_INTERNAL(testnum, inst, result, mem, vs3, vs2, vlen, mlen, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, vs3, vlen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, mem, mlen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v1, (a3), v2 ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(mem, RD_ADDR, mlen, lh, sh, ebits/8); \
    eqm(result, mem, mlen);

/**
 * vsxb.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 */
#define TEST_VSXB_V(testnum, result, mem, vs3, vs2, vlen, mlen) \
  TEST_VSXx_V_INTERNAL(testnum, vsxb.v, result, mem, vs3, vs2, vlen, mlen, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vsxh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 */
#define TEST_VSXH_V(testnum, result, mem, vs3, vs2, vlen, mlen) \
  TEST_VSXx_V_INTERNAL(testnum, vsxh.v, result, mem, vs3, vs2, vlen, mlen, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vsxw.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 */
#define TEST_VSXW_V(testnum, result, mem, vs3, vs2, vlen, mlen) \
  TEST_VSXx_V_INTERNAL(testnum, vsxw.v, result, mem, vs3, vs2, vlen, mlen, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vsxe.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSXE_V(testnum, result, mem, vs3, vs2, vlen, mlen, ebits, eqm) \
  TEST_VSXx_V_INTERNAL(testnum, vsxe.v, result, mem, vs3, vs2, vlen, mlen, ebits, vle.v, eqm)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSXx_V_MASK_INTERNAL(testnum, inst, result, mem, vs3, vs2, vlen, mlen, mask, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, vs3, vlen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, mem, mlen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v2, (a2) ; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  inst v1, (a3), v2, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(mem, RD_ADDR, mlen, lh, sh, ebits/8); \
    eqm(result, mem, mlen);

/**
 * vsxb.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSXB_V_MASK(testnum, result, mem, vs3, vs2, vlen, mlen, mask) \
  TEST_VSXx_V_MASK_INTERNAL(testnum, vsxb.v, result, mem, vs3, vs2, vlen, mlen, mask, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vsxh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSXH_V_MASK(testnum, result, mem, vs3, vs2, vlen, mlen, mask) \
  TEST_VSXx_V_MASK_INTERNAL(testnum, vsxh.v, result, mem, vs3, vs2, vlen, mlen, mask, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vsxh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSXW_V_MASK(testnum, result, mem, vs3, vs2, vlen, mlen, mask) \
  TEST_VSXx_V_MASK_INTERNAL(testnum, vsxw.v, result, mem, vs3, vs2, vlen, mlen, mask, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vsxe.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs3       start addr for source vector
 * @vs2       start addr for index vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSXE_V_MASK(testnum, result, mem, vs3, vs2, vlen, mlen, mask, ebits, eqm) \
  TEST_VSXx_V_MASK_INTERNAL(testnum, vsxe.v, result, mem, vs3, vs2, vlen, mlen, mask, ebits, vle.v, eqm)


/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @soff1     address offset for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSXx_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VSXB_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSXx_V_MISALIGNED_BASE( testnum, vsxb.v, vlen, soff1, 8)

#define TEST_VSXH_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSXx_V_MISALIGNED_BASE( testnum, vsxh.v, vlen, soff1, 16)

#define TEST_VSXW_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSXx_V_MISALIGNED_BASE( testnum, vsxw.v, vlen, soff1, 32)

#define TEST_VSXE_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VSXx_V_MISALIGNED_BASE( testnum, vsxe.v, vlen, soff1, ebits)


/**
 * Misaligned stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @rs2       stride
 * @ebits     element size in bits
 */
#define TEST_VSXx_V_MISALIGNED_STRIDE( testnum, inst, vlen, vs2, ebits, ldins) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_OFFSET, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
  li a1, RS1_ADDR ; \
  la a2, RS2_ADDR ; \
  ldins v2, (a2) ; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VSXB_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VSXx_V_MISALIGNED_STRIDE( testnum, vsxb.v, vlen, vs2, 8, vlb.v)

#define TEST_VSXH_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VSXx_V_MISALIGNED_STRIDE( testnum, vsxh.v, vlen, vs2, 16, vlh.v)

#define TEST_VSXW_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VSXx_V_MISALIGNED_STRIDE( testnum, vsxw.v, vlen, vs2, 32, vlw.v)

#define TEST_VSXE_V_MISALIGNED_STRIDE( testnum, vlen, vs2, ebits) \
  TEST_VSXx_V_MISALIGNED_STRIDE( testnum, vsxe.v, vlen, vs2, ebits, vle.v)


/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSXx_V_ACCESS_FAULT( testnum, inst, vlen, vs3, vs2, ebits, ldins) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
  li a1, vs3; \
  la a2, RS2_ADDR ; \
  ldins v2, (a2) ; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VSXB_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSXx_V_ACCESS_FAULT( testnum, vsxb.v, vlen, vs3, rs2, 8, vlb.v)

#define TEST_VSXH_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSXx_V_ACCESS_FAULT( testnum, vsxh.v, vlen, vs3, rs2, 16, vlh.v)

#define TEST_VSXW_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSXx_V_ACCESS_FAULT( testnum, vsxw.v, vlen, vs3, rs2, 32, vlw.v)

#define TEST_VSXE_V_ACCESS_FAULT( testnum, vlen, vs3, rs2, ebits) \
  TEST_VSXx_V_ACCESS_FAULT( testnum, vsxe.v, vlen, vs3, rs2, ebits, vle.v)




#endif // __TEST_MACROS_VSXX_V_H
