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
 * Tests for vext.x.v instructions
 * 
 *    vext.x.v rd, vs2, rs1
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VEXT_X_V_H
#define __TEST_MACROS_VEXT_X_V_H

#include "test_macros_v.h"
#include "test_macros.h"


/**
 * General functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      the source rs1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * xldins     inst to load scale
 */
#define TEST_VEXT_X_V_INTERNAL(testnum, result, val1, val2, vlen, ebits, ldins, xldins) \
test_ ## testnum: \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, result; \
    la a3, val2 ; \
    xldins a4, (a2);\
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    xldins a5, (a3);\
    PERF_BEGIN() \
  vext.x.v a6, v1, a5 ; \
    PERF_END(testnum ## _ ## vlen) \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne a6, a4, tofail_ ## testnum;   \

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @val2      addr of source xreg rs2
 * @vlen      vector length
 */
#define TEST_VEXT_X_V_HF(testnum, result, val1, val2, vlen) \
  TEST_VEXT_X_V_INTERNAL(testnum, result, val1, val2, vlen, 16, vlh.v, lw)


/**
 * General functional
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      addr for rs1, a scale idx number
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @xldins     inst to load scale
 */
#define TEST_VEXT_X_V_RD_EQU_RS1_INTERNAL(testnum, result, val1, val2, vlen, ebits, ldins, xldins) \
test_ ## testnum: \
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
    la a2, result; \
    la a3, val2 ; \
    xldins a4, (a3);\
    xldins a5, (a2);\
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  vext.x.v a4, v1, a4 ; \
    PERF_END(testnum ## _ ## vlen) \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne a4, a5, tofail_ ## testnum;   \

/**
 * Functional test. rd=rs1
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @val2      addr of source xreg rs2
 * @vlen      vector length
 */
#define TEST_VEXT_X_V_RD_EQU_RS1_HF(testnum, result, val1, val2, vlen) \
  TEST_VEXT_X_V_RD_EQU_RS1_INTERNAL(testnum, result, val1, val2, vlen, 16, vlh.v, lw)

#endif // __TEST_MACROS_VFMIN_VV_H
