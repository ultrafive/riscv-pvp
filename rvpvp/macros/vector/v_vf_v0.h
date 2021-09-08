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
 * Tests for insn v, v, f v0 instructions
 * 
 * Authors: Hao Chen
 */
#ifndef __TEST_MACROS_V_VF_V0_H
#define __TEST_MACROS_V_VF_V0_H

#include "test_macros_v.h"

/**
 * Insns vd, vs2, rs1 v0
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vd         register index for vd
 * @vs2         register index for vs2
 * @val1      start addr for source float value
 * @val2      start addr for source vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @stins     inst for store source vector
 * @eqm       macro for compare two vectors
 * @val0     start addr for source v0 
 */
#define TEST_V_VF_V0_SIMPLE_INTERNAL(testnum, inst, vd, vs2, result, val1, val2, vlen, ebits, vldins, vstins, fldins, val0, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum ; \
    COPY(RS2_ADDR, val2, vlen, lh, sh, 2) ; \
    COPY(MASK_ADDR, val0, vlen, lh, sh, 2) ; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, RS2_ADDR ; \
    la a3, MASK_ADDR ; \
    la a4, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits ; \
  fldins fa1, (a1) ; \
  vldins v0, (a3) ; \
  vldins VREG_ ## vs2, (a2) ; \
    PERF_BEGIN() \
  inst VREG_ ## vd, VREG_ ## vs2, fa1, v0 ; \
    PERF_END(testnum ## _ ## vlen) \
  vstins VREG_ ## vd, (a4) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2) ; \
    eqm(result, test_ ## testnum ## _data, vlen) ; \
    .pushsection .data ; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0 ; \
    .popsection

/**
 * insns vd, vs2, rs1 v0   short
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd         register index for vd
 * @vs2         register index for vs2
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      mask vector
 */
#define TEST_V_VF_V0_SH_SIMPLE(testnum, inst, vd, vs2, result, val1, val2, vlen, val0) \
  TEST_V_VF_V0_SIMPLE_INTERNAL(testnum, inst, vd, vs2, result, val1, val2, vlen, 16, vlh.v, vsh.v, flw, val0, VV_SH_CHECK_EQ)

/**
 * insns vd, vs2, rs1 v0   long int
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd         register index for vd
 * @vs2         register index for vs2
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      mask vector
 */
#define TEST_V_VF_V0_SD_SIMPLE(testnum, inst, vd, vs2, result, val1, val2, vlen, val0) \
  TEST_V_VF_V0_SIMPLE_INTERNAL(testnum, inst, vd, vs2, result, val1, val2, vlen, 64, vle.v, vse.v, fld, val0, VV_SD_CHECK_EQ)

/**
 * insns vd, vs2, rs1 v0   half
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd         register index for vd
 * @vs2         register index for vs2
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      mask vector
 */
#define TEST_V_VF_V0_HF_SIMPLE(testnum, inst, vd, vs2, result, val1, val2, vlen, val0) \
  TEST_V_VF_V0_SIMPLE_INTERNAL(testnum, inst, vd, vs2, result, val1, val2, vlen, 16, vlh.v, vsh.v, flw, val0, VV_HF_CHECK_EQ)

/**
 * insns vd, vs2, rs1 v0   double
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vd         register index for vd
 * @vs2         register index for vs2
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      start addr for source vector
 * @vlen      vector length
 * @val0      mask vector
 */
#define TEST_V_VF_V0_DF_SIMPLE(testnum, inst, vd, vs2, result, val1, val2, vlen, val0) \
  TEST_V_VF_V0_SIMPLE_INTERNAL(testnum, inst, vd, vs2, result, val1, val2, vlen, 64, vle.v, vse.v, fld, val0, VV_DF_CHECK_EQ)

#endif // __TEST_MACROS_VSX_V_H
