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
 * Tests for vpopc.m instructions
 * 
 *    vpopc.m rd, vs2, vm
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VPOPC_M_H
#define __TEST_MACROS_VPOPC_M_H

#include "test_macros_v.h"
#include "test_macros.h"


/**
 * General functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector rs1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * xldins     inst to load scale
 */
#define TEST_V_POPC_INTERNAL( testnum, result, val1, vlen, ebits, ldins, xldins) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, result; \
    xldins a3, (a2);\
  vsetvli a4, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  vpopc.m a4, v1; \
    PERF_END(testnum ## _ ## vlen) \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne a4, a3, tofail_ ## testnum;   \


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_POPC_HF(testnum, result, val1, vlen) \
  TEST_V_POPC_INTERNAL(testnum, result, val1, vlen, 16, vlh.v, lw)



/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @val0      start addr for source vector mask
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @xldins    inst to load scale to x-reg.
 */
#define TEST_V_POPC_MASK_INTERNAL(testnum, result, val1, val0, vlen, ebits, ldins, xldins) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, result; \
    xldins a3, (a2);\
    la a4, MASK_ADDR ; \
  vsetvli a5, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  vpopc.m a5, v1, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne a5, a3, tofail_ ## testnum;   \


/**
 * Functional tests with mask enabled.
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @v0t       start addr for source v0(mask vector)
 * @vlen      vector length
 */
#define TEST_V_POPC_MASK_HF( testnum, result, val1, v0t, vlen) \
  TEST_V_POPC_MASK_INTERNAL(testnum, result, val1, v0t, vlen, 16, vlh.v, lw)


/**
 * Functional tests with mask and using v0 as vs1.
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val0      start addr for source vector mask
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @xldins    inst to load scale to x-reg.
 */
#define TEST_V_POPC_MASK_INTERNAL_V0_V0T(testnum, result, val0, vlen, ebits, ldins, xldins) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2); \
    li a0, vlen ; \
    la a2, result; \
    xldins a3, (a2);\
    la a4, MASK_ADDR ; \
  vsetvli a5, a0, e ## ebits; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  vpopc.m a5, v0, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne a5, a3, tofail_ ## testnum;   \

/**
 * Functional tests with mask enabled ans v0 as vs1.
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @v0t       start addr for source v0(mask vector)
 * @vlen      vector length
 */
#define TEST_V_POPC_MASK_V0_V0T_HF( testnum, result, v0t, vlen) \
  TEST_V_POPC_MASK_INTERNAL_V0_V0T(testnum, result, v0t, vlen, 16, vlh.v, lw)


#endif // __TEST_MACROS_VPOPC_M_H