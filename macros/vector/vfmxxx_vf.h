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
 * Tests for vfmxxx.vf instructions
 * 
 *    vfmxxx.vf vd, vs2, rs1[, v0.t]
 * 
 * Authors: Pascal Ouyang
 */
#ifndef __TEST_MACROS_VFMXXX_VF_H
#define __TEST_MACROS_VFMXXX_VF_H

#include "test_macros_v.h"

#define VFMXXX_VF_CHECK_EQ_HF_ATOL  0.0001
#define VFMXXX_VF_CHECK_EQ_HF_RTOL  50
#define VFMXXX_VF_CHECK_EQ_HF(vec1, vec2, vlen) \
    VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, VFMXXX_VF_CHECK_EQ_HF_ATOL, VFMXXX_VF_CHECK_EQ_HF_RTOL, 1)

/*******************************************************************************
 * vfmxxx.vf Functional tests without mask
 ******************************************************************************/

/**
 * vfmxxx.vf Functional tests without mask
 *  *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vd        start addr for original vd vector
 * @val1      start addr for source scalar float
 * @val2      start addr for source vector 2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFMXXX_VF_INTERNAL(testnum, inst, result, vd, val1, val2, vlen, ebits, ldins, stins, fldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, vd, vlen, lh, sh, ebits/8); \
    la a1, val1 ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    fldins fa1, (a1) ; \
    ldins v2, (a2) ; \
    ldins v3, (a3) ; \
    PERF_BEGIN() \
  inst v3, fa1, v2 ; \
    PERF_END(testnum ## _ ## vlen) \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfmxxx.vf Functional tests without mask
 *  *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 */
#define TEST_VFMXXX_VF_HF(testnum, inst, vlen) \
  TEST_VFMXXX_VF_INTERNAL(testnum, inst, \
      t##testnum##_vd, t##testnum##_vds, t##testnum##_rs1, t##testnum##_vs2, \
      vlen, 16, vlh.v, vsh.v, flw, VFMXXX_VF_CHECK_EQ_HF)


/*******************************************************************************
 * vfmxxx.vf Functional tests without mask, vd = vs2
 ******************************************************************************/

/**
 * vfmxxx.vf Functional tests without mask
 * 
 *      vd = vs2
 * 
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source scalar float
 * @val2      start addr for source vector 2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFMXXX_VF_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, fldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    la a1, val1 ; \
    la a2, RS2_ADDR ; \
    fldins fa1, (a1) ; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v2, fa1, v2 ; \
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
 * vfmxxx.vf Functional tests without mask
 * 
 *    vd = vs2
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source scalar float
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VFMXXX_VF_DEST_EQ_SRC2_HF(testnum, inst, vlen) \
  TEST_VFMXXX_VF_DEST_EQ_SRC2_INTERNAL(testnum, inst, \
      t##testnum##_vd, t##testnum##_rs1, t##testnum##_vs2, \
      vlen, 16, vlh.v, vsh.v, flw, VFMXXX_VF_CHECK_EQ_HF)

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/

/**
 * vfmxxx.vf Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source scalar float
 * @val2      start addr for source vector 2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFMXXX_VF_MASK_INTERNAL(testnum, inst, result, vd, val1, val2, mask, vlen, ebits, ldins, stins, fldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, vd, vlen, lh, sh, ebits/8); \
    la a1, val1 ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
    fldins fa1, (a1) ; \
    ldins v2, (a2) ; \
    ldins v3, (a3) ; \
    ldins v0, (a4) ; \
    PERF_BEGIN() \
  inst v3, fa1, v2, v0.t ; \
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
 * vfmxxx.vf Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source scalar float
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VFMXXX_VF_MASK_HF(testnum, inst, vlen) \
  TEST_VFMXXX_VF_MASK_INTERNAL(testnum, inst, \
      t##testnum##_vd, t##testnum##_vds, t##testnum##_rs1, t##testnum##_vs2, \
      t##testnum##_mask, \
      vlen, 16, vlh.v, vsh.v, flw, VFMXXX_VF_CHECK_EQ_HF)

#endif // __TEST_MACROS_VFMXXX_VF_H
