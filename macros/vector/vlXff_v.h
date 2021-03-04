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
#ifndef __TEST_MACROS_VLxFF_V_H
#define __TEST_MACROS_VLxFF_V_H

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
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLxFF_V_INTERNAL(testnum, inst, result, val1, vlen, slen, ebits, stins, eqm) \
test_ ## testnum: \
  COPY(RS1_ADDR, val1, slen, lh, sh, ebits/8); \
  li a0, vlen; \
  la a1, RS1_ADDR; \
  la a2, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  inst v1, (a1) ; \
  stins v1, (a2) ; \
  COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vlhff.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLHFF_V(testnum, result, val1, vlen, slen) \
  TEST_VLxFF_V_INTERNAL(testnum, vlhff.v, result, val1, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlhuff.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLHUFF_V(testnum, result, val1, vlen, slen) \
  TEST_VLxFF_V_INTERNAL(testnum, vlhuff.v, result, val1, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)


/**
 * vleff.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VLEFF_V(testnum, result, val1, vlen, slen, ebits, eqm) \
  TEST_VLxFF_V_INTERNAL(testnum, vleff.v, result, val1, vlen, slen, ebits, vse.v, eqm)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLxFF_V_MASK_INTERNAL(testnum, inst, result, val1, vlen, slen, mask, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, slen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, slen, lh, sh, ebits/8); \
    la a4, MASK_ADDR ; \
    li a0, vlen; \
    la a1, RS1_ADDR; \
    la a2, RD_ADDR; \
    vsetvli t0, a0, e ## ebits; \
    ldins v0, (a4) ; \
    fmv.s.x ft0, x0; \
    vfmv.v.f v1, ft0; \
    PERF_BEGIN() \
    inst v1, (a1), v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    stins v1, (a2) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection



/**
 * vlhff.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 */
#define TEST_VLHFF_V_MASK(testnum, result, val1, vlen, slen, mask) \
  TEST_VLxFF_V_MASK_INTERNAL(testnum, vlhff.v, result, val1, vlen, slen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlhuff.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 */
#define TEST_VLHUFF_V_MASK(testnum, result, val1, vlen, slen, mask) \
  TEST_VLxFF_V_MASK_INTERNAL(testnum, vlhuff.v, result, val1, vlen, slen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vleff.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VLEFF_V_MASK(testnum, result, val1, vlen, slen, mask, ebits, eqm) \
  TEST_VLxFF_V_MASK_INTERNAL(testnum, vleff.v, result, val1, vlen, slen, mask, ebits, vle.v ,vse.v, eqm)


/**
 * Tests without mask to unaligned address
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLxFF_V_UNALIGNED_INTERNAL(testnum, inst, result, val1, vlen, slen, ebits, stins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_MISALIGNED_LOAD, test_ ## testnum ## _end); \
    \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, slen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a3, test_ ## testnum ## _data ; \
  vsetvli t0, a0, e ## ebits; \
  inst v1, (a1) ; \
  j fail; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
    .fill 1, 1, 0; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection \
test_ ## testnum ## _end: \


/**
 * vlhff.v Tests without mask to unaligned address
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLHFF_V_UNALIGNED(testnum, result, val1, vlen, slen) \
  TEST_VLxFF_V_UNALIGNED_INTERNAL(testnum, vlhff.v, result, val1, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlhuff.v Tests without mask to unaligned address
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLHUFF_V_UNALIGNED(testnum, result, val1, vlen, slen) \
  TEST_VLxFF_V_UNALIGNED_INTERNAL(testnum, vlhuff.v, result, val1, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)

/**
 * vleff.v Tests without mask to unaligned address
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VLEFF_V_UNALIGNED(testnum, result, val1, vlen, slen, ebits, eqm) \
  TEST_VLxFF_V_UNALIGNED_INTERNAL(testnum, vleff.v, result, val1, vlen, slen, ebits, vse.v, eqm)

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
 * @nvl       new vl after vl*ff execute with access fault
 * @vlen      vector length
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLxFF_V_MODIFY_VL(testnum, inst, result, val1, offset, nvl, vlen, slen, ebits, stins, eqm) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(L1B_ADDR+offset, val1, slen, lh, sh, ebits/8); \
  la a1, L1B_ADDR+offset; \
  la a2, RD_ADDR; \
  li a0, vlen; \
  vsetvli t0, a0, e ## ebits; \
    PERF_BEGIN() \
  inst v1, (a1) ; \
    PERF_END(testnum ## _ ## vlen) \
  csrr t1, vl; \
  li t2, nvl; \
  bne t1, t2, fail; \
  stins v1, (a2) ; \
  COPY(test_ ## testnum ## _data, RD_ADDR, slen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, nvl); \
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
 * @slen      source data length
 */
#define TEST_VLHFF_V_MODIFY_VL(testnum, result, val1, offset, nvl, vlen, slen) \
  TEST_VLxFF_V_MODIFY_VL(testnum, vlhff.v, result, val1, offset, nvl, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)

#define TEST_VLHUFF_V_MODIFY_VL(testnum, result, val1, offset, nvl, vlen, slen) \
  TEST_VLxFF_V_MODIFY_VL(testnum, vlhuff.v, result, val1, offset, nvl, vlen, slen, 16, vsh.v, VV_SH_CHECK_EQ)

#define TEST_VLEFF_V_MODIFY_VL(testnum, result, val1, offset, nvl, vlen, slen, ebits, eqm) \
  TEST_VLxFF_V_MODIFY_VL(testnum, vleff.v, result, val1, offset, nvl, vlen, slen, ebits, vse.v, eqm)


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
#define TEST_VLxFF_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VLBFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlbff.v, vlen, soff1, 8)

#define TEST_VLHFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlhff.v, vlen, soff1, 16)

#define TEST_VLWFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlwff.v, vlen, soff1, 32)

#define TEST_VLBUFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlbuff.v, vlen, soff1, 8)

#define TEST_VLHUFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlhuff.v, vlen, soff1, 16)

#define TEST_VLWUFF_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vlwuff.v, vlen, soff1, 32)

#define TEST_VLEFF_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VLxFF_V_MISALIGNED_BASE( testnum, vleff.v, vlen, soff1, ebits)

/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VLxFF_V_ACCESS_FAULT( testnum, inst, vlen, src1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, src1; \
  inst v1, (a1); \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VLBFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlbff.v, vlen, src1, 8)

#define TEST_VLHFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlhff.v, vlen, src1, 16)

#define TEST_VLWFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlwff.v, vlen, src1, 32)

#define TEST_VLBUFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlbuff.v, vlen, src1, 8)

#define TEST_VLHUFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlhuff.v, vlen, src1, 16)

#define TEST_VLWUFF_V_ACCESS_FAULT( testnum, vlen, src1) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vlwuff.v, vlen, src1, 32)

#define TEST_VLEFF_V_ACCESS_FAULT( testnum, vlen, src1, ebits) \
  TEST_VLxFF_V_ACCESS_FAULT( testnum, vleff.v, vlen, src1, ebits)

#endif // __TEST_MACROS_VLxFF_V_H
