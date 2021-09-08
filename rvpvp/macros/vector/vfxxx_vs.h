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
 * Tests for vfxxx.vs instructions
 * 
 *    vfxxx.vs vd, vs2, vs1[, v0.t]
 * 
 * Authors: Hao Chen
 */
#ifndef __TEST_MACROS_VFXXX_VS_H
#define __TEST_MACROS_VFXXX_VS_H

#include "test_macros_v.h"

/*******************************************************************************
 * vfxxx.vs vd, vs2, vs1 Functional tests without mask
 ******************************************************************************/

#define VFXXX_VS_HF_ATOL 0.001
#define VFXXX_VS_HF_RTOL 1

#define VV_CHECK_EQ_HF_VFXXX_VS(vec1, vec2, vlen) \
    VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, VFXXX_VS_HF_ATOL, VFXXX_VS_HF_RTOL, vlen + 1)

/**
 * vfxxx.vs vd, vs2, vs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @val3      start addr for source vector 3
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_INTERNAL(testnum, inst, result, val1, val2, val3, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    COPY(RD_PRELOAD_ADDR, val3, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a3, RD_PRELOAD_ADDR ; \
  ldins v1, (a1) ; \
  ldins v2, (a2) ; \
  ldins v3, (a3) ; \
    PERF_BEGIN() \
  inst v3, v2, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a4, RD_ADDR ; \
  stins v3, (a4); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfxxx.vs vd, vs2, vs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @val3      start addr for source vector 3
 * @vlen      vector length
 */
#define TEST_VFXXX_VS_HF(testnum, inst, result, val1, val2, val3, vlen) \
  TEST_VFXXX_VS_INTERNAL(testnum, inst, result, val1, val2, val3, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_SH(testnum, inst, result, val1, val2, val3, vlen) \
  TEST_VFXXX_VS_INTERNAL(testnum, inst, result, val1, val2, val3, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vfxxx.vs vd, vs1, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vfxxx.vs vd, vs1, vs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val3      start addr for source vector 3
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_SRC2_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val3, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    COPY(RD_PRELOAD_ADDR, val3, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
    la a2, RD_PRELOAD_ADDR ; \
  ldins v1, (a1) ; \
  ldins v3, (a2) ; \
    PERF_BEGIN() \
  inst v3, v1, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
  stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfxxx.vs vd, vs1, vs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val3      start addr for source vector 3
 * @vlen      vector length
 */
#define TEST_VFXXX_VS_SRC2_EQ_SRC1_HF(testnum, inst, result, val1, val3, vlen) \
  TEST_VFXXX_VS_SRC2_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val3, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_SRC2_EQ_SRC1_SH(testnum, inst, result, val1, val3, vlen) \
  TEST_VFXXX_VS_SRC2_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val3, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vfxxx.vv vs1, vs1, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vfxxx.vs vs1, vs1, vs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC12_INTERNAL(testnum, inst, result, val1, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v1, v1, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
  stins v1, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfxxx.vs vs1, vs1, vs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC12_HF(testnum, inst, result, val1, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC12_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_DEST_EQ_SRC12_SH(testnum, inst, result, val1, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC12_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)
/*******************************************************************************
 * vfxxx.vv vs1, vs2, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vfxxx.vs vs1, vs2, vs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    ldins v1, (a1) ; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v1, v2, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
  stins v1, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfxxx.vs vs1, vs2, vs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC1_HF(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_DEST_EQ_SRC1_SH(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)
/*******************************************************************************
 * vfxxx.vv vs2, vs2, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vfxxx.vs vs2, vs2, vs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
  ldins v1, (a1) ; \
  ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v2, v2, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
  stins v2, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfxxx.vs vs2, vs2, vs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VFXXX_VS_DEST_EQ_SRC2_HF(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_DEST_EQ_SRC2_SH(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VS_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @val2      start addr for source vector2
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @val3      start addr dest vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFXXX_VS_MASK_INTERNAL(testnum, inst, result, val1, val2, vlen, val0, val3, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, vlen, lh, sh, 2) ; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2) ; \
    COPY(RD_PRELOAD_ADDR, val3, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_PRELOAD_ADDR ; \
  ldins v1, (a1) ; \
  ldins v2, (a2) ; \
  ldins v0, (a0) ; \
  ldins v3, (a3) ; \
    PERF_BEGIN() \
  inst v3, v2, v1, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    la a3, RD_ADDR ; \
  stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
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
 * @val1      start addr for source vector1
 * @val2      start addr for source vector2
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @val3      start addr dest vector
 */
#define TEST_VFXXX_VS_MASK_HF(testnum, inst, result, val1, val2, vlen, val0, val3) \
  TEST_VFXXX_VS_MASK_INTERNAL(testnum, inst, result, val1, val2, vlen, val0, val3, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFXXX_VS)

#define TEST_VFXXX_VS_MASK_SH(testnum, inst, result, val1, val2, vlen, val0, val3) \
  TEST_VFXXX_VS_MASK_INTERNAL(testnum, inst, result, val1, val2, vlen, val0, val3, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#endif // __TEST_MACROS_VFXXX_VV_H
