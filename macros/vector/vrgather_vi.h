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
 * Tests for vrgather.vi instructions
 * 
 *    vrgather.vi vd, vs2, uimm[, v0.t] # vd[i] = (imm>= VLMAX) ? 0 : vs2[uimm]
 * 
 * Authors: Honghua.Cao
 */
#ifndef __TEST_MACROS_VRGATHER_VI_H
#define __TEST_MACROS_VRGATHER_VI_H

#include "test_macros_v.h"
#include "exception.h"

/*******************************************************************************
 * vrgather.vi vd, vs2, uimm Functional tests without mask
 ******************************************************************************/

/**
 * vrgather.vi vd, vs2, uimm Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VRGATHER_VI_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, 64 ; \
	COPY(RS2_ADDR, vs2_orig, 64, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
    inst v3, v2, uimm ; \
    PERF_END(testnum ## _ ## vlen) \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vrgather.vi vd, vs2, uimm HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 */
#define TEST_VRGATHER_VI_HF(testnum, inst, result, uimm, vs2, vs2_orig, vlen) \
  TEST_VRGATHER_VI_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vrgather.vv vs2, vs2, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vrgather.vi vd, vs2, uimm Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VRGATHER_VI_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    li a0, 64 ; \
    COPY(RS2_ADDR, vs2_orig, 64, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR; \
    la a3, RD_ADDR ; \
    ldins v2, (a2) ; \
    inst v2, v2, uimm ; \
    j fail; \
    stins v2, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection \
test_ ## testnum ## _end: \

/**
 * vrgather.vi vd, vs2, uimm HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 */
#define TEST_VRGATHER_VI_DEST_EQ_SRC2_HF(testnum, inst, result, uimm, vs2, vs2_orig, vlen) \
  TEST_VRGATHER_VI_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @vd_orig      start addr dest vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VRGATHER_VI_MASK_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask, vd_orig, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, 64 ; \
    vsetvli t0, a0, e ## ebits; \
    COPY(RS2_ADDR, vs2_orig, 64, lh, sh, 2); \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd_orig, vlen, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    ldins v3, (a3) ; \
    PERF_BEGIN() \
    inst v3, v2, uimm, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
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
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @vd_orig      start addr dest vector
 */
#define TEST_VRGATHER_VI_MASK_HF(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask, vd_orig) \
  TEST_VRGATHER_VI_MASK_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask, vd_orig, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

  /**
 * vrgather.vi vd, vs2, uimm, v0.t Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @vd_orig      start addr dest vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VRGATHER_VI_MASK_DEST_EQ_SRC0_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    li a0, 64 ; \
    COPY(RS2_ADDR, vs2_orig, 64, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    ldins v2, (a2) ; \
    \
    li a0, vlen ; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    vsetvli t0, a0, e ## ebits; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    inst v0, v2, uimm, v0.t ; \
    j fail; \
    stins v0, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection \
test_ ## testnum ## _end: \

/**
 * vrgather.vi vd, vs2, uimm, v0.t HF Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @uimm      unshort immediate data
 * @vs2      start addr for source vector2 with vl=vlen
 * @vs2_orig      start addr for source vector2 with vl=64
 * @vlen      vector lengthmask
 * @mask      start addr for source vector mask
 */
#define TEST_VRGATHER_VI_MASK_DEST_EQ_SRC0_HF(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask) \
  TEST_VRGATHER_VI_MASK_DEST_EQ_SRC0_INTERNAL(testnum, inst, result, uimm, vs2, vs2_orig, vlen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


#endif // __TEST_MACROS_VRGATHER_VI_H
