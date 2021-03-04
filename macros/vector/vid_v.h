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
 * Tests for vid.v instructions
 * 
 *    vid.v vd, vm
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VID_V_H
#define __TEST_MACROS_VID_V_H

#include "test_macros_v.h"
#include "test_macros.h"


/**
 * General functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VID_V_INTERNAL(testnum, result, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a3, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
    PERF_BEGIN() \
  vid.v v2 ; \
    PERF_END(testnum ## _ ## vlen) \
  stins v2, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vlen      vector length
 */
#define TEST_VID_V_HF(testnum, result, vlen) \
  TEST_VID_V_INTERNAL(testnum, result, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)



/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr for dest vector
 * @val0      start addr for source vector mask
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 */
#define TEST_VID_V_MASK_INTERNAL(testnum, result, vd, val0, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    COPY(RD_ADDR, vd, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RD_ADDR ; \
    la a4, MASK_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  vid.v v1, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
  stins v1, (a1); \
    COPY(vd, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, vd, vlen); \


#define TEST_VID_V_MASK_HF( testnum, result, vd, v0t, vlen) \
  TEST_VID_V_MASK_INTERNAL(testnum, result, vd, v0t, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr for dest vector
 * @val0      start addr for source vector mask
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 */
#define TEST_VID_V_MASK_VD_EQU_VM_INTERNAL(testnum, result, vd, val0, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    COPY(RD_ADDR, vd, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RD_ADDR ; \
    la a2, MASK_ADDR; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a2) ; \
    PERF_BEGIN() \
  vid.v v0, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
  stins v0, (a1); \
    COPY(vd, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, vd, vlen); \

/**
 * Functional tests with mask and vd=vm
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr of dest vector
 * @v0t       start addr of mask vector
 * @vlen      vector length
 */
#define TEST_VID_V_MASK_VD_EQU_VM_HF(testnum, result, vd, v0t, vlen) \
  TEST_VID_V_MASK_VD_EQU_VM_INTERNAL(testnum, result, vd, v0t, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#endif // __TEST_MACROS_VID_V_H
