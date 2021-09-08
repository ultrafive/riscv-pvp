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
 * Tests for vfcvt.f.xu.v and vfcvt.f.x.v instructions
 * 
 * Authors: Hao Chen
 */
#ifndef __TEST_MACROS_VFCVT_F_H
#define __TEST_MACROS_VFCVT_F_H

#include "test_macros_v.h"

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v      with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        vector register for vd
 * @vs2      vector register for vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vs2
 * @val0      start addr for source v0.t
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @vldins     inst for load source vector
 * @vstins     inst for store source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFCVT_F_MSK_INTERNAL(testnum, inst, vd, vs2, preload, result, val2, val0, vlen, ebits, vldins, vstins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2) ; \
    COPY(RD_PRELOAD_ADDR, preload, vlen, lh, sh, 2) ; \
    li a0, vlen; \
    la a1, RS2_ADDR; \
    la a2, MASK_ADDR; \
    la a3, RD_PRELOAD_ADDR; \
    la a4, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  vldins VREG_ ## vs2, (a1); \
  vldins VREG_ ## vd, (a3); \
  vldins v0, (a2); \
    PERF_BEGIN() \
  inst VREG_ ## vd, VREG_ ## vs2, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
  vstins VREG_ ## vd, (a4); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v      disable mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        vector register for vd
 * @vs2      vector register for vs2
 * @result    start addr for test result
 * @val2      start addr for source vs2
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @vldins     inst for load source vector
 * @vstins     inst for store source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VFCVT_F_NOMASK_INTERNAL(testnum, inst, vd, vs2, result, val2, vlen, ebits, vldins, vstins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    li a0, vlen; \
    la a1, RS2_ADDR; \
    la a2, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  vldins VREG_ ## vs2, (a1); \
    PERF_BEGIN() \
  inst VREG_ ## vd, VREG_ ## vs2; \
    PERF_END(testnum ## _ ## vlen) \
  vstins VREG_ ## vd, (a2); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection


/**
 * vfcvt.f.xu.v and vfcvt.f.x.v   short
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_SH_MASK(testnum, inst, vd, vs2, preload, result, val2, val0, vlen) \
  TEST_VFCVT_F_MSK_INTERNAL(testnum, inst, vd, vs2, preload, result, val2, val0, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v    long int
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_SD_MASK(testnum, inst, vd, vs2, preload, result, val2, val0, vlen) \
    TEST_VFCVT_F_MSK_INTERNAL(testnum, inst, vd, vs2, preload, result, val2, val0, vlen, 64, vle.v, vse.v, VV_SD_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v   half
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_HF_MASK(testnum, inst, vd, vs2, preload, result, val2, val0, vlen) \
    TEST_VFCVT_F_MSK_INTERNAL(testnum, inst, vd, vs2, preload, result, val2, val0, vlen, 16, vlh.v, vsh.v, VV_HF_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v   double
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_DF_MASK(testnum, inst, vd, vs2, preload, result, val2, val0, vlen) \
    TEST_VFCVT_F_MSK_INTERNAL(testnum, inst, vd, vs2, preload, result, val2, val0, vlen, 64, vle.v, vse.v, VV_DF_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v  disable mask   short
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_SH_NOMASK(testnum, inst, vd, vs2, result, val2, vlen) \
  TEST_VFCVT_F_NOMASK_INTERNAL(testnum, inst, vd, vs2, result, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v    disable mask   long int
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_SD_NOMASK(testnum, inst, vd, vs2, result, val2, vlen) \
    TEST_VFCVT_F_NOMASK_INTERNAL(testnum, inst, vd, vs2, result, val2, vlen, 64, vle.v, vse.v, VV_SD_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v   disable mask   half
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_HF_NOMASK(testnum, inst, vd, vs2, result, val2, vlen) \
    TEST_VFCVT_F_NOMASK_INTERNAL(testnum, inst, vd, vs2, result, val2, vlen, 16, vlh.v, vsh.v, VV_HF_CHECK_EQ)

/**
 * vfcvt.f.xu.v and vfcvt.f.x.v   disable mask    double
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd        register vd
 * @vs2        register vs2
 * @preload  preload to vd for mask test
 * @result    start addr for test result
 * @val2      start addr for source vector
 * @val0      start addr for source v0.t
 * @vlen      vector length
 */
#define TEST_VFCVT_F_DF_NOMASK(testnum, inst, vd, vs2, result, val2, vlen) \
    TEST_VFCVT_F_NOMASK_INTERNAL(testnum, inst, vd, vs2, result, val2, vlen, 64, vle.v, vse.v, VV_DF_CHECK_EQ)

#endif // __TEST_MACROS_V_F_H
