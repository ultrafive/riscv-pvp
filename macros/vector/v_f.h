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
 * Tests for insn v, f instructions
 * 
 * Authors: Hao Chen
 */
#ifndef __TEST_MACROS_V_F_H
#define __TEST_MACROS_V_F_H

#include "test_macros_v.h"

/**
 * Insns vd, f
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source float value
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @stins     inst for store source vector
 * @fldins   float load insn
 * @eqm       macro for compare two vectors
 */
#define TEST_V_F_SIMPLE_INTERNAL(testnum, inst, result, val1, vlen, ebits, vstins, fldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen; \
    la a1, val1; \
    la a3, RD_ADDR; \
  vsetvli t0, a0, e ## ebits; \
    fldins ft0, (a1); \
    PERF_BEGIN() \
  inst v1, ft0; \
    PERF_END(testnum ## _ ## vlen) \
  vstins v1, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection


/**
 * insns vd, rs1   short
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_V_F_SH_SIMPLE(testnum, inst, result, val1, vlen) \
  TEST_V_F_SIMPLE_INTERNAL(testnum, inst, result, val1, vlen, 16, vsh.v, flw, VV_SH_CHECK_EQ)

/**
 * insns vd, rs1    long int
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_V_F_SD_SIMPLE(testnum, inst, result, val1, vlen) \
  TEST_V_F_SIMPLE_INTERNAL(testnum, inst, result, val1, vlen, 64, vse.v, fld, VV_SD_CHECK_EQ)

/**
 * insns vd,  rs1   half
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_V_F_HF_SIMPLE(testnum, inst, result, val1, vlen) \
  TEST_V_F_SIMPLE_INTERNAL(testnum, inst, result, val1, vlen, 16, vsh.v, flw, VV_HF_CHECK_EQ)

/**
 * insns vd, rs1   double
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @vlen      vector length
 */
#define TEST_V_F_DF_SIMPLE(testnum, inst, result, val1, vlen) \
  TEST_V_F_SIMPLE_INTERNAL(testnum, inst, result, val1, vlen, 64, vse.v, fld, VV_DF_CHECK_EQ)

#endif // __TEST_MACROS_V_F_H
