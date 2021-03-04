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
 *    vs*.v vs3, (rs1), vm
 * 
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VSX_V_H
#define __TEST_MACROS_VSX_V_H

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
 * @val1      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSx_V_INTERNAL(testnum, inst, result, val1, vlen, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, ebits/8); \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v1, (a3) ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vsb.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VSB_V(testnum, result, val1, vlen) \
  TEST_VSx_V_INTERNAL(testnum, vsb.v, result, val1, vlen, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vsh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VSH_V(testnum, result, val1, vlen) \
  TEST_VSx_V_INTERNAL(testnum, vsh.v, result, val1, vlen, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vsw.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VSW_V(testnum, result, val1, vlen) \
  TEST_VSx_V_INTERNAL(testnum, vsw.v, result, val1, vlen, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vse.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSE_V(testnum, result, val1, vlen, ebits, eqm) \
  TEST_VSx_V_INTERNAL(testnum, vse.v, result, val1, vlen, ebits, vle.v, eqm)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSx_V_MASK_INTERNAL(testnum, inst, result, val1, vlen, mask, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, ebits/8); \
    la a1, RS1_ADDR ; \
    la a4, MASK_ADDR ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
  fmv.s.x ft0, x0; \
  vfmv.v.f v2, ft0; \
  vsh.v v2, (a3) ; \
    PERF_BEGIN() \
  inst v1, (a3), v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vsb.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSB_V_MASK(testnum, result, val1, vlen, mask) \
  TEST_VSx_V_MASK_INTERNAL(testnum, vsb.v, result, val1, vlen, mask, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vsh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSH_V_MASK(testnum, result, val1, vlen, mask) \
  TEST_VSx_V_MASK_INTERNAL(testnum, vsh.v, result, val1, vlen, mask, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vsh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSW_V_MASK(testnum, result, val1, vlen, mask) \
  TEST_VSx_V_MASK_INTERNAL(testnum, vsw.v, result, val1, vlen, mask, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vse.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSE_V_MASK(testnum, result, val1, vlen, mask, ebits, eqm) \
  TEST_VSx_V_MASK_INTERNAL(testnum, vse.v, result, val1, vlen, mask, ebits, vle.v, eqm)


/*******************************************************************************
 * Exception tests
 ******************************************************************************/

/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @soff1     address offset for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSX_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VSB_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSX_V_MISALIGNED_BASE( testnum, vsb.v, vlen, soff1, 8)

#define TEST_VSH_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSX_V_MISALIGNED_BASE( testnum, vsh.v, vlen, soff1, 16)

#define TEST_VSW_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSX_V_MISALIGNED_BASE( testnum, vsw.v, vlen, soff1, 32)

#define TEST_VSE_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VSX_V_MISALIGNED_BASE( testnum, vse.v, vlen, soff1, ebits)

/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSX_V_ACCESS_FAULT( testnum, inst, vlen, src1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, src1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VSB_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VSX_V_ACCESS_FAULT( testnum, vsb.v, vlen, src1, 8)

#define TEST_VSH_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VSX_V_ACCESS_FAULT( testnum, vsh.v, vlen, src1, 16)

#define TEST_VSW_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VSX_V_ACCESS_FAULT( testnum, vsw.v, vlen, src1, 32)

#define TEST_VSE_V_ACCESS_FAULT( testnum, vlen, src1, ebits) \
  TEST_VSX_V_ACCESS_FAULT( testnum, vse.v, vlen, src1, ebits)

#endif // __TEST_MACROS_VSX_V_H
