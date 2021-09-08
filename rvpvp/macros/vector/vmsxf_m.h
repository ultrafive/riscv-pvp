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
 * Tests for vmsxf.m and viota.m instructions
 * 
 *    vmsxf.m vd, vs2, vm
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VMSXF_M_H
#define __TEST_MACROS_VMSXF_M_H

#include "test_macros_v.h"
#include "test_macros.h"


/**
 * General functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_V_MSXF_M_INTERNAL(testnum, inst, result, val1, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v2, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v2, (a2); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_VMSXF_M_HF(testnum, inst, result, val1, vlen)  \
  TEST_V_MSXF_M_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


/**
 * General functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_V_MSXF_M_DEST_EQU_SRC_INTERNAL(testnum, inst, result, val1, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v1, v1 ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v1, (a2); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_VMSXF_M_DEST_EQU_SRC_HF(testnum, inst, result, val1, vlen)  \
  TEST_V_MSXF_M_DEST_EQU_SRC_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested
 * @result    start addr for test result
 * @vd        start result to save the result. pre-inited with random.
 * @val1      start addr for source vector1
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @ebits     element bits, 8 for by3e, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_V_MSXF_M_MASK_INTERNAL(testnum, inst, result, vd, val1, vlen, val0, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, RD_ADDR ; \
    la a3, MASK_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a3) ; \
  ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v2, v1, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v2, (a2); \
    COPY(vd, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, vd, vlen); \

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test golden result
 * @vd        start addr to save the result.pre-initd.
 * @val1      start addr for source vector1
 * @vlen      vector length
 * @val0      mask vector v0
 */
#define TEST_V_MSXF_M_MASK_HF(testnum, inst, result, vd, val1, vlen, val0) \
  TEST_V_MSXF_M_MASK_INTERNAL(testnum, inst, result, vd, val1, vlen, val0, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


/**
 * Functional tests with mask and with v0 as vs2
 *
 * @testnum   test case number
 * @inst      the inst to be tested
 * @result    start addr for test result
 * @vd        start addr to save the result.
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_V_MSXF_M_MASK_VS2_EQU_V0T_INTERNAL(testnum, inst, result, vd, vlen, val0, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RD_ADDR ; \
    la a2, MASK_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a2) ; \
  ldins v2, (a1) ; \
    PERF_BEGIN() \
  inst v2, v0, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v2, (a1); \
    COPY(vd, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, vd, vlen); \

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @vd        start addr to save the result
 * @vlen      vector length
 * @val0      mask vector v0
 */
#define TEST_V_MSXF_M_MASK_VS2_EQU_V0T_HF(testnum, inst, result, vd, vlen, val0) \
  TEST_V_MSXF_M_MASK_VS2_EQU_V0T_INTERNAL(testnum, inst, result, vd, vlen, val0, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


/**
 * Functional tests with mask and with v0 as vs2
 *
 * @testnum   test case number
 * @inst      the inst to be tested
 * @result    start addr for test result
 * @vd        start addr to save the rlt.
 * @val1      start addr for source vector1
 * @vlen      vector length
 * @val0      start addr for source vector mask
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_V_MSXF_M_MASK_VD_EQU_VS2_EQU_V0T_INTERNAL(testnum, inst, result, vd, vlen, val0, ebits, ldins, stins, eqm) \
 test_ ## testnum: \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RD_ADDR ; \
    la a2, MASK_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a2) ; \
    PERF_BEGIN() \
  inst v0, v0, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v0, (a1); \
    COPY(vd, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, vd, vlen); \

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      the inst to be tested.
 * @result    start addr for test result
 * @vd        start addr to save the result.
 * @val1      start addr for source vector1
 * @vlen      vector length
 * @val0      mask vector v0
 */
#define TEST_V_MSXF_M_MASK_VD_EQU_VS2_EQU_V0T_HF(testnum, inst, result, vd, vlen, val0) \
  TEST_V_MSXF_M_MASK_VD_EQU_VS2_EQU_V0T_INTERNAL(testnum, inst, result, vd, vlen, val0, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


#endif // __TEST_MACROS_VMSXF_M_H
