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
 * Tests for vslideup.vx instructions
 * 
 *    vslideup.vx vd, vs2, rs1 [, v0.t] # vd[i+rs1] = vs2[i] 
 * 
 * Authors: Honghua.Cao
 */
#ifndef __TEST_MACROS_VSLIDEUP_VX_H
#define __TEST_MACROS_VSLIDEUP_VX_H

#include "test_macros_v.h"
#include "exception.h"

/*******************************************************************************
 * vslideup.vx vd, vs2, rs1 Functional tests without mask
 ******************************************************************************/

/**
 * vslideup.vx vd, vs2, rs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, vlen, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd_orig, vlen, lh, sh, 2); \
    li a0, vlen ; \
    vsetvli t0, a0, e ## ebits; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    ldins v3, (a3) ; \
    PERF_BEGIN() \
    inst v3, v2, a1; \
    PERF_END(testnum ## _ ## vlen) \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vslideup.vx vd, vs2, rs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 */
#define TEST_VSLIDEUP_VX_HF(testnum, inst, result, rs1, vs2, vd_orig, vlen) \
  TEST_VSLIDEUP_VX_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, vlen, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vslideup.vx vd, vs2, rs1 Functional tests without mask vl=0
 ******************************************************************************/

/**
 * vslideup.vx vd, vs2, rs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_VL_EQ0_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, last_vlen, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    la a3, RD_ADDR ; \
    \
    li a0, last_vlen ; \
    vsetvli t0, a0, e ## ebits ; \
    COPY(RD_ADDR, vd_orig, last_vlen, lh, sh, 2); \
    la a2, RD_ADDR ; \
    ldins v3, (a2) ; \
    \
    COPY(RS2_ADDR, vs2, last_vlen, lh, sh, 2); \
    li a0, 0 ; \
    vsetvli t0, a0, e ## ebits ; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
    inst v3, v2, a1 ; \
    PERF_END(testnum ## _ ## vlen) \
    \
    li a0, last_vlen ; \
    vsetvli t0, a0, e ## ebits; \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, last_vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, last_vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill last_vlen, (ebits/8), 0; \
    .popsection

/**
 * vslideup.vx vd, vs2, rs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 */
#define TEST_VSLIDEUP_VX_VL_EQ0_HF(testnum, inst, result, rs1, vs2, vd_orig, last_vlen) \
  TEST_VSLIDEUP_VX_VL_EQ0_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, last_vlen, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)

/*******************************************************************************
 * vslideup.vx vs2, vs2, vs1 Functional tests without mask
 ******************************************************************************/

/**
 * vslideup.vx vd, vs2, rs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, rs1, vs2, vlen, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    li a0, vlen ; \
    vsetvli t0, a0, e ## ebits; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
  	inst v2, v2, a1 ; \
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
 * vslideup.vx vd, vs2, rs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 */
#define TEST_VSLIDEUP_VX_DEST_EQ_SRC2_HF(testnum, inst, result, rs1, vs2, vlen) \
  TEST_VSLIDEUP_VX_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, rs1, vs2, vlen, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_MASK_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, vlen, mask, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd_orig, vlen, lh, sh, 2); \
    li a0, vlen ; \
    vsetvli t0, a0, e ## ebits; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR; \
    la a3, RD_ADDR; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    ldins v3, (a3) ; \
    PERF_BEGIN() \
  inst v3, v2, a1, v0.t ; \
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
 * @rs1      start addr for source vector1
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 */
#define TEST_VSLIDEUP_VX_MASK_HF(testnum, inst, result, rs1, vs2, vd_orig, vlen, mask) \
  TEST_VSLIDEUP_VX_MASK_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, vlen, mask, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)


/*******************************************************************************
 * vslideup.vx vd, vs2, rs1 Functional tests without mask vl=0
 ******************************************************************************/

/**
 * vslideup.vx vd, vs2, rs1 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_MASK_VL_EQ0_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, last_vlen, mask, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RD_ADDR, vd_orig, 64, lh, sh, 2); \
    \
    li a0, last_vlen ; \
    vsetvli t0, a0, e ## ebits ; \
    la a2, RD_ADDR ; \
    ldins v3, (a2) ; \
    \
    li a0, 0 ; \
    vsetvli t0, a0, e ## ebits ; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR ; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    PERF_BEGIN() \
    inst v3, v2, a1, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    \
    li a0, last_vlen ; \
    vsetvli t0, a0, e ## ebits; \
    stins v3, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, last_vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, last_vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill last_vlen, (ebits/8), 0; \
    .popsection

/**
 * vslideup.vx vd, vs2, rs1 HF Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source scalar uint32
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 */
#define TEST_VSLIDEUP_VX_MASK_VL_EQ0_HF(testnum, inst, result, rs1, vs2, vd_orig, last_vlen, mask) \
  TEST_VSLIDEUP_VX_MASK_VL_EQ0_INTERNAL(testnum, inst, result, rs1, vs2, vd_orig, last_vlen, mask, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)

  /**
 * vslideup.vx vd, vs2, rs1, v0.t Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source vector1
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC0_INTERNAL(testnum, inst, result, rs1, vs2, vlen, mask, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    li a0, vlen ; \
    vsetvli t0, a0, e ## ebits; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR ; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    PERF_BEGIN() \
  	inst v0, v2, a1, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    stins v0, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection


/**
 * vslideup.vx vd, vs2, rs1, v0.t HF Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source vector1
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 */
#define TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC0_HF(testnum, inst, result, rs1, vs2, vlen, mask) \
  TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC0_INTERNAL(testnum, inst, result, rs1, vs2, vlen, mask, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)

  /**
 * vslideup.vx vs2, vs2, rs1, v0.t Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source vector1
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, rs1, vs2, vlen, mask, ebits, ldins, stins, xldins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    COPY(RS2_ADDR, vs2, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    li a0, vlen ; \
    vsetvli t0, a0, e ## ebits; \
    la a1, rs1 ; \
    la a2, RS2_ADDR ; \
    la a0, MASK_ADDR ; \
    la a3, RD_ADDR ; \
    xldins a1, 0(a1) ; \
    ldins v2, (a2) ; \
    ldins v0, (a0) ; \
    inst v2, v2, a1, v0.t ; \
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
 * vslideup.vx vs2, vs2, rs1, v0.t HF Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @rs1      start addr for source vector1
 * @vs2      start addr for source vector2 with vl=vlen
 * @vd_orig   start addr for origin dest vector
 * @vlen      vector length
 * @mask      start addr for source vector mask
 */
#define TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC2_HF(testnum, inst, result, rs1, vs2, vlen, mask) \
  TEST_VSLIDEUP_VX_MASK_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, rs1, vs2, vlen, mask, 16, vlh.v, vsh.v, lw, VV_SH_CHECK_EQ)


#endif // __TEST_MACROS_VSLIDEUP_VX_H
