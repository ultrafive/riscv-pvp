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
 * Tests for vl*.v instructions
 * 
 *    vl*.v vl3, (rs1), vm
 * 
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VLX_V_H
#define __TEST_MACROS_VLX_V_H

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
#define TEST_VLx_V_INTERNAL(testnum, inst, result, val1, vlen, ebits, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
    PERF_BEGIN() \
  inst v1, (a1) ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v1, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vlh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VLH_V(testnum, result, val1, vlen) \
  TEST_VLx_V_INTERNAL(testnum, vlh.v, result, val1, vlen, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlhu.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VLHU_V(testnum, result, val1, vlen) \
  TEST_VLx_V_INTERNAL(testnum, vlhu.v, result, val1, vlen, 16, vsh.v, VV_SH_CHECK_EQ)


/**
 * vle.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VLE_V(testnum, result, val1, vlen, ebits, eqm) \
  TEST_VLx_V_INTERNAL(testnum, vle.v, result, val1, vlen, ebits, vse.v, eqm)

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
#define TEST_VLx_V_MASK_INTERNAL(testnum, inst, result, val1, vlen, mask, ebits, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a4, MASK_ADDR ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  inst v0, (a4) ; \
  vfsub.vv v1, v1, v1 ; \
    PERF_BEGIN() \
  inst v1, (a1), v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v1, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection



/**
 * vlh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VLH_V_MASK(testnum, result, val1, vlen, mask) \
  TEST_VLx_V_MASK_INTERNAL(testnum, vlh.v, result, val1, vlen, mask, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VLHU_V_MASK(testnum, result, val1, vlen, mask) \
  TEST_VLx_V_MASK_INTERNAL(testnum, vlhu.v, result, val1, vlen, mask, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vle.v Functional tests with mask
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
#define TEST_VLE_V_MASK(testnum, result, val1, vlen, mask, ebits, eqm) \
  TEST_VLx_V_MASK_INTERNAL(testnum, vle.v, result, val1, vlen, mask, ebits, vse.v, eqm)

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
#define TEST_VLx_V_INTERSECTION_INTERNAL(testnum, inst, result, val1, itsc_reg, vlen, ebits, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
    PERF_BEGIN() \
  inst v1, (a1) ; \
    PERF_END(testnum ## _ ## vlen) \
    sub itsc_reg, itsc_reg, itsc_reg; \
    bnez itsc_reg, fail; \
  stins v1, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vlh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VLH_V_INTERSECT(testnum, result, val1, itsc_reg, vlen) \
  TEST_VLx_V_INTERSECTION_INTERNAL(testnum, vlh.v, result, val1, itsc_reg, vlen, 16, vsh.v, VV_SH_CHECK_EQ)

#define TEST_VLHU_V_INTERSECT(testnum, result, val1, itsc_reg, vlen) \
  TEST_VLx_V_INTERSECTION_INTERNAL(testnum, vlhu.v, result, val1, itsc_reg, vlen, 16, vsh.v, VV_SH_CHECK_EQ)

#define TEST_VLE_V_INTERSECT(testnum, result, val1, itsc_reg, vlen, ebits, eqm) \
  TEST_VLx_V_INTERSECTION_INTERNAL(testnum, vle.v, result, val1, itsc_reg, vlen, ebits, vse.v, eqm)


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
#define TEST_VLX_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VLB_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlb.v, vlen, soff1, 8)

#define TEST_VLH_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlh.v, vlen, soff1, 16)

#define TEST_VLW_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlw.v, vlen, soff1, 32)

#define TEST_VLBU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlbu.v, vlen, soff1, 8)

#define TEST_VLHU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlhu.v, vlen, soff1, 16)

#define TEST_VLWU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vlwu.v, vlen, soff1, 32)

#define TEST_VLE_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VLX_V_MISALIGNED_BASE( testnum, vle.v, vlen, soff1, ebits)

/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VLX_V_ACCESS_FAULT( testnum, inst, vlen, src1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, src1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VLB_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlb.v, vlen, src1, 8)

#define TEST_VLH_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlh.v, vlen, src1, 16)

#define TEST_VLW_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlw.v, vlen, src1, 32)

#define TEST_VLBU_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlbu.v, vlen, src1, 8)

#define TEST_VLHU_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlhu.v, vlen, src1, 16)

#define TEST_VLWU_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vlwu.v, vlen, src1, 32)

#define TEST_VLE_V_ACCESS_FAULT( testnum, vlen, src1, ebits) \
  TEST_VLX_V_ACCESS_FAULT( testnum, vle.v, vlen, src1, ebits)

#endif // __TEST_MACROS_VLX_V_H
