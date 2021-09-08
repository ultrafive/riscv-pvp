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
 * Tests for vs*.v instructions
 * 
 *    vss*.v vs3, (rs1), rs2, vm
 * 
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VSSX_V_H
#define __TEST_MACROS_VSSX_V_H

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
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSx_V_INTERNAL(testnum, inst, result, mem, vs3, rs2, vlen, dlen, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, vs3, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, mem, dlen, lh, sh, ebits/8); \
    la a1, RS1_ADDR ; \
    la a2, rs2 ; \
    lw a2, 0(a2) ; \
    la a3, RD_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    PERF_BEGIN() \
  inst v1, (a3), a2 ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(mem, RD_ADDR, dlen, lh, sh, ebits/8); \
    eqm(result, mem, vlen);

/**
 * vssb.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 */
#define TEST_VSSB_V(testnum, result, mem, vs3, rs2, vlen, dlen) \
  TEST_VSSx_V_INTERNAL(testnum, vssb.v, result, mem, vs3, rs2, vlen, dlen, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vssh.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 */
#define TEST_VSSH_V(testnum, result, mem, vs3, rs2, vlen, dlen) \
  TEST_VSSx_V_INTERNAL(testnum, vssh.v, result, mem, vs3, rs2, vlen, dlen, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vssw.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3      start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 */
#define TEST_VSSW_V(testnum, result, mem, vs3, rs2, vlen, dlen) \
  TEST_VSSx_V_INTERNAL(testnum, vssw.v, result, mem, vs3, rs2, vlen, dlen, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vsse.v Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSE_V(testnum, result, mem, vs3, rs2, vlen, dlen, ebits, eqm) \
  TEST_VSSx_V_INTERNAL(testnum, vsse.v, result, mem, vs3, rs2, vlen, dlen, ebits, vle.v, eqm)

/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSx_V_MASK_INTERNAL(testnum, inst, result, mem, vs3, rs2, vlen, dlen, mask, ebits, ldins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    COPY(RS1_ADDR, vs3, vlen, lh, sh, ebits/8); \
    COPY(RD_ADDR, mem, dlen, lh, sh, ebits/8); \
    COPY(RS2_ADDR, rs2, vlen, lh, sh, ebits/8); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, ebits/8); \
    li a0, vlen ; \
    la a1, RS1_ADDR ; \
    la a2, RS2_ADDR ; \
    lw a2, 0(a2) ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
    PERF_BEGIN() \
  inst v1, (a3), a2, v0.t ; \
    PERF_END(testnum ## _ ## vlen) \
    COPY(mem, RD_ADDR, dlen, lh, sh, ebits/8); \
    eqm(result, mem, vlen);

/**
 * vssb.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSSB_V_MASK(testnum, result, mem, vs3, rs2, vlen, dlen, mask) \
  TEST_VSSx_V_MASK_INTERNAL(testnum, vssb.v, result, mem, vs3, rs2, vlen, dlen, mask, 8, vlb.v, VV_SB_CHECK_EQ)

/**
 * vssh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSSH_V_MASK(testnum, result, mem, vs3, rs2, vlen, dlen, mask) \
  TEST_VSSx_V_MASK_INTERNAL(testnum, vssh.v, result, mem, vs3, rs2, vlen, dlen, mask, 16, vlh.v, VV_SH_CHECK_EQ)

/**
 * vssh.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VSSW_V_MASK(testnum, result, mem, vs3, rs2, vlen, dlen, mask) \
  TEST_VSSx_V_MASK_INTERNAL(testnum, vssw.v, result, mem, vs3, rs2, vlen, dlen, mask, 32, vlw.v, VV_SW_CHECK_EQ)

/**
 * vsse.v Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @mem       start addr for mem before store
 * @vs3       start addr for source vector
 * @rs2       start addr for stride
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two vectors
 */
#define TEST_VSSE_V_MASK(testnum, result, mem, vs3, rs2, vlen, dlen,mask, ebits, eqm) \
  TEST_VSSx_V_MASK_INTERNAL(testnum, vsse.v, result, mem, vs3, rs2, vlen, dlen, mask, ebits, vle.v, eqm)


/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @soff1     address offset for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSSx_V_MISALIGNED_BASE( testnum, inst, vlen, soff1, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR + soff1; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VSSB_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSSx_V_MISALIGNED_BASE( testnum, vssb.v, vlen, soff1, 8)

#define TEST_VSSH_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSSx_V_MISALIGNED_BASE( testnum, vssh.v, vlen, soff1, 16)

#define TEST_VSSW_V_MISALIGNED_BASE( testnum, vlen, soff1) \
  TEST_VSSx_V_MISALIGNED_BASE( testnum, vssw.v, vlen, soff1, 32)

#define TEST_VSSE_V_MISALIGNED_BASE( testnum, vlen, soff1, ebits) \
  TEST_VSSx_V_MISALIGNED_BASE( testnum, vsse.v, vlen, soff1, ebits)


/**
 * Misaligned stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @rs2       stride
 * @ebits     element size in bits
 */
#define TEST_VSSx_V_MISALIGNED_STRIDE( testnum, inst, vlen, rs2, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_MISALIGNED_OFFSET, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  la a2, rs2 ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, RS1_ADDR ; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \

#define TEST_VSSB_V_MISALIGNED_STRIDE( testnum, vlen, rs2) \
  TEST_VSSx_V_MISALIGNED_STRIDE( testnum, vssb.v, vlen, rs2, 8)

#define TEST_VSSH_V_MISALIGNED_STRIDE( testnum, vlen, rs2) \
  TEST_VSSx_V_MISALIGNED_STRIDE( testnum, vssh.v, vlen, rs2, 16)

#define TEST_VSSW_V_MISALIGNED_STRIDE( testnum, vlen, rs2) \
  TEST_VSSx_V_MISALIGNED_STRIDE( testnum, vssw.v, vlen, rs2, 32)

#define TEST_VSSE_V_MISALIGNED_STRIDE( testnum, vlen, rs2, ebits) \
  TEST_VSSx_V_MISALIGNED_STRIDE( testnum, vsse.v, vlen, rs2, ebits)


/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @vlen      vector length
 * @src1      address for source operand 1
 * @ebits     element size in bits
 */
#define TEST_VSSx_V_ACCESS_FAULT( testnum, inst, vlen, vs3, rs2, ebits) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_RVV_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  li a0, vlen ; \
  la a2, rs2 ; \
  vsetvli t0, a0, e ## ebits; \
  li a1, vs3; \
  inst v1, (a1), a2; \
  j fail; \
test_ ## testnum ## _end: \


#define TEST_VSSB_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSSx_V_ACCESS_FAULT( testnum, vssb.v, vlen, vs3, rs2, 8)

#define TEST_VSSH_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSSx_V_ACCESS_FAULT( testnum, vssh.v, vlen, vs3, rs2, 16)

#define TEST_VSSW_V_ACCESS_FAULT( testnum, vlen, vs3, rs2) \
  TEST_VSSx_V_ACCESS_FAULT( testnum, vssw.v, vlen, vs3, rs2, 32)

#define TEST_VSSE_V_ACCESS_FAULT( testnum, vlen, vs3, rs2, ebits) \
  TEST_VSSx_V_ACCESS_FAULT( testnum, vsse.v, vlen, vs3, rs2, ebits)


#endif // __TEST_MACROS_VSSX_V_H
