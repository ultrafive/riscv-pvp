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
 * Tests for vfexp.v instructions
 * 
 *    vfexp.v vd, vs2, vm# vector-vector exponent, vd[i]=exp(vs2[i])
 * 
 * Authors: Honghua Cao
 */
#ifndef __TEST_MACROS_VEXP_V_H
#define __TEST_MACROS_VEXP_V_H

#include "test_macros_v.h"

// The absolute torlance, for float16, the atol is 1e0-4
#define VFEXP_V_HF_ATOL 0.0
// The relative torlance as binary comparsion for two float16 number
#define VFEXP_V_HF_RTOL 5

#define VV_CHECK_EQ_HF_VFEXP_V(vec1, vec2, vlen) \
  VV_CHECK_EQ_HF(vec1, vec2, vlen, VFEXP_V_HF_ATOL, VFEXP_V_HF_RTOL); \

/*******************************************************************************
 * Functional tests without mask
 ******************************************************************************/

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs2      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFEXP_V_INTERNAL(testnum, inst, result, vs2, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    la a1, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    sub a0, a0, t0; \
    PERF_BEGIN() \
    inst v2, v1; \
    PERF_END(testnum ## _ ## vlen) \
    stins v2, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfexp.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs2      start addr for source vector
 * @vlen      vector length
 */
#define TEST_VFEXP_V_HF(testnum, result, vs2, vlen) \
  TEST_VFEXP_V_INTERNAL(testnum, vfexp.v, result, vs2, vlen, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFEXP_V)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs2      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFEXP_V_MASK_INTERNAL(testnum, inst, result, vs2, vlen, mask, vd_orig, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd_orig, vlen, lh, sh, 2); \
    la a1, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
    la a5, RD_ADDR ; \
    \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    ldins v0, (a4) ; \
    ldins v2, (a5) ; \
    sub a0, a0, t0; \
    PERF_BEGIN() \
    inst v2, v1, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
    stins v2, (a3); \
	\
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfexp.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs2      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VFEXP_V_MASK_HF(testnum, result, vs2, vlen, mask, vd_orig) \
  TEST_VFEXP_V_MASK_INTERNAL(testnum, vfexp.v, result, vs2, vlen, mask, vd_orig, 16, vlh.v, vsh.v, VV_CHECK_EQ_HF_VFEXP_V)


#endif // __TEST_MACROS_VFEXP_V_H
