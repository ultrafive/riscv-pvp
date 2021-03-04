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
 * Tests for vfclass.v instructions
 * 
 *    vfclass.v vd, vs2[, v0.t]
 * 
 * Authors: Bin Jiang
 */
#ifndef __TEST_MACROS_VFCLASS_V_H
#define __TEST_MACROS_VFCLASS_V_H

#include "test_macros_v.h"

/*******************************************************************************
 * vfclass.v vd, vs2 Functional tests without mask
 ******************************************************************************/

/**
 * vfclass.v vd, vs2 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFCLASS_V_INTERNAL(testnum, inst, result, val2, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v3, v2 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfclass.v vd, vs2 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VFCLASS_V_HF(testnum, inst, result, val2, vlen) \
  TEST_VFCLASS_V_INTERNAL(testnum, inst, result, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vfclass.v vs2, vs2 Functional tests without mask
 ******************************************************************************/

/**
 * vfclass.v vs2, vs2 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFCLASS_V_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val2, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v2, v2 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
    stins v2, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfclass.v vs2, vs2 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VFCLASS_V_DEST_EQ_SRC2_HF(testnum, inst, result, val2, vlen) \
  TEST_VFCLASS_V_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @val3      start addr dest vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFCLASS_V_MASK_INTERNAL(testnum, inst, result, val2, vlen, val0, val3, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RD_ADDR, val3, vlen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, val0, vlen, lh, sh, ebits/8); \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    ldins v3, (a3) ; \
    PERF_BEGIN() \
  inst v3, v2, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * HF Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @val3      start addr dest vector
 */
#define TEST_VFCLASS_V_MASK_HF(testnum, inst, result, val2, vlen, val0, val3) \
  TEST_VFCLASS_V_MASK_INTERNAL(testnum, inst, result, val2, vlen, val0, val3, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#endif // __TEST_MACROS_VFCLASS_V_H
