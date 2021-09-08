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
 * Tests for vls*.v instructions
 * 
 *    vlxS*.v vs3, (rs1), vm
 * 
 * Authors: kai ren
 */
#ifndef __TEST_MACROS_VLSX_V_H
#define __TEST_MACROS_VLSX_V_H

#include "test_macros_v.h"
#include "exception.h"

/*******************************************************************************
 * Functional tests without mask
 ******************************************************************************/

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @stins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLXx_V_INTERNAL(testnum, inst, result, val1, val2, vlen, slen, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, slen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, val2, slen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a3, RD_ADDR ; \
 \
  vsetvli t0, a0, e ## ebits; \
    ldins v2, (a2) ; \
    PERF_BEGIN() \
  inst v1, (a1), v2; \
    PERF_END(testnum ## _ ## vlen) \
  stins v1, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vlxh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLXH_V(testnum, result, val1, val2, vlen, slen) \
  TEST_VLXx_V_INTERNAL(testnum, vlxh.v, result, val1, val2, vlen, slen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlxe.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLXE_V(testnum, result, val1, val2, vlen, slen) \
  TEST_VLXx_V_INTERNAL(testnum, vlxe.v, result, val1, val2, vlen, slen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlxhu.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 */
#define TEST_VLXHU_V(testnum, result, val1, val2, vlen, slen) \
  TEST_VLXx_V_INTERNAL(testnum, vlxhu.v, result, val1, val2, vlen, slen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load v0 mask
 * @stins     inst for store source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VLXx_V_MASK_INTERNAL(testnum, inst, result, val1, val2, vlen, slen, mask, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, val1, slen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, val2, slen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, slen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    la a4, MASK_ADDR ; \
  \
    vsetvli t0, a0, e ## ebits; \
    ldins v2, (a2) ; \
    ldins v0, (a4) ; \
    fmv.s.x ft0, x0; \
    vfmv.v.f v1, ft0; \
    la a3, RD_ADDR ; \
    PERF_BEGIN() \
    inst v1, (a1), v2, v0.t; \
    PERF_END(testnum ## _ ## vlen) \
    stins v1, (a3); \
    \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, ebits/8); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vlxe.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 */
#define TEST_VLXE_V_MASK(testnum, result, val1, val2, vlen, slen, mask) \
  TEST_VLXx_V_MASK_INTERNAL(testnum, vlxe.v, result, val1, val2, vlen, slen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlxh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 */
#define TEST_VLXH_V_MASK(testnum, result, val1, val2, vlen, slen, mask) \
  TEST_VLXx_V_MASK_INTERNAL(testnum, vlxh.v, result, val1, val2, vlen, slen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vlxhu.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector
 * @val2      indices for base address
 * @vlen      vector length
 * @slen      source data length
 * @mask      start addr for mask vector
 */
#define TEST_VLXHU_V_MASK(testnum, result, val1, val2, vlen, slen, mask) \
  TEST_VLXx_V_MASK_INTERNAL(testnum, vlxhu.v, result, val1, val2, vlen, slen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)


/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @soff1     address offset for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VLXx_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VLXB_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxb.v, vlen, soff1, 8)

#define TEST_VLXH_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxh.v, vlen, soff1, 16)

#define TEST_VLXW_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxw.v, vlen, soff1, 32)

#define TEST_VLXBU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxbu.v, vlen, soff1, 8)

#define TEST_VLXHU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxhu.v, vlen, soff1, 16)

#define TEST_VLXWU_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxwu.v, vlen, soff1, 32)

#define TEST_VLXE_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VLXx_V_MISALIGNED_BASE( testnum, vlxe.v, vlen, soff1, ebits)


/**
 * Misaligned stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @rs2       stride
 * @ebits     element size in bits
 */
#define TEST_VLXx_V_MISALIGNED_STRIDE( testnum, inst, vlen, vs2, ebits, ldins) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_OFFSET, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
  li a1, RS1_ADDR ; \
  la a2, RS2_ADDR ; \
  ldins v2, (a2) ; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VLXB_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxb.v, vlen, vs2, 8, vlb.v)

#define TEST_VLXH_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxh.v, vlen, vs2, 16, vlh.v)

#define TEST_VLXW_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxw.v, vlen, vs2, 32, vlw.v)

#define TEST_VLXBU_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxbu.v, vlen, vs2, 8, vlb.v)

#define TEST_VLXHU_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxhu.v, vlen, vs2, 16, vlh.v)

#define TEST_VLXWU_V_MISALIGNED_STRIDE( testnum, vlen, vs2) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxwu.v, vlen, vs2, 32, vlw.v)

#define TEST_VLXE_V_MISALIGNED_STRIDE( testnum, vlen, vs2, ebits) \
  TEST_VLXx_V_MISALIGNED_STRIDE( testnum, vlxe.v, vlen, vs2, ebits, vle.v)


/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VLXx_V_ACCESS_FAULT( testnum, inst, vlen, vs3, vs2, ebits, ldins) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  COPY(RS2_ADDR, vs2, vlen, lh, sh, ebits/8); \
  li a1, vs3; \
  la a2, RS2_ADDR ; \
  ldins v2, (a2) ; \
  inst v1, (a1), v2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VLXB_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxb.v, vlen, vs3, rs2, 8, vlb.v)

#define TEST_VLXH_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxh.v, vlen, vs3, rs2, 16, vlh.v)

#define TEST_VLXW_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxw.v, vlen, vs3, rs2, 32, vlw.v)

#define TEST_VLXBU_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxbu.v, vlen, vs3, rs2, 8, vlb.v)

#define TEST_VLXHU_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxhu.v, vlen, vs3, rs2, 16, vlh.v)

#define TEST_VLXWU_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxwu.v, vlen, vs3, rs2, 32, vlw.v)

#define TEST_VLXE_V_ACCESS_FAULT( testnum, vlen, vs3, rs2, ebits) \
  TEST_VLXx_V_ACCESS_FAULT( testnum, vlxe.v, vlen, vs3, rs2, ebits, vle.v)



#endif // __TEST_MACROS_VSX_V_H
