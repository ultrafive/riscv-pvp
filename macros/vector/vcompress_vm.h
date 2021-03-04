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
 * Tests for vfsqrt.v instructions
 * 
 *    vcompress.vm v2, v1, v0# Compress into vd elements of vs2 where vs1 is enable
 * 
 * Authors: Honghua Cao
 */
#ifndef __TEST_MACROS_VCOMPRESS_VM_H
#define __TEST_MACROS_VCOMPRESS_VM_H

#include "test_macros_v.h"
#include "exception.h"

/*******************************************************************************
 * Functional tests with mask
 ******************************************************************************/
/**
 * vcompress.vm v2, v1, v0 Functional tests without mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VCOMPRESS_VM_INTERNAL(testnum, inst, result, vs1, vlen, mask, vd_orig, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, vs1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    COPY(RD_ADDR, vd_orig, vlen, lh, sh, 2); \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR; \
    la a4, MASK_ADDR ; \
    la a5, RD_ADDR ; \
    \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    ldins v0, (a4) ; \
    ldins v2, (a5) ; \
    sub a0, a0, t0; \
    PERF_BEGIN() \
    inst v2, v1, v0; \
    PERF_END(testnum ## _ ## vlen) \
    stins v2, (a3); \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

/**
 * vcompress.vm v2, v1, v0 Functional tests with mask
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VCOMPRESS_VM_HF(testnum, result, vs1, vlen, mask, vd_orig) \
  TEST_VCOMPRESS_VM_INTERNAL(testnum, vcompress.vm, result, vs1, vlen, mask, vd_orig, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vcompress.vm v1, v1, v0 Functional tests without mask, vd = vs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VCOMPRESS_VM_DEST_EQ_SRC1_INTERNAL(testnum, inst, result, vs1, vlen, mask, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, vs1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
    \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    ldins v0, (a4) ; \
    sub a0, a0, t0; \
    inst v1, v1, v0; \
    j fail; \
    stins v1, (a3) ; \
    COPY(test_ ## testnum ## _data, RD_ADDR, vlen, lh, sh, 2); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection \
test_ ## testnum ## _end: \

/**
 * vcompress.vm v1, v1, v0 Functional tests with mask, vd = vs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VCOMPRESS_VM_DEST_EQ_SRC1_HF(testnum, result, vs1, vlen, mask) \
  TEST_VCOMPRESS_VM_DEST_EQ_SRC1_INTERNAL(testnum, vcompress.vm, result, vs1, vlen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vcompress.vm v0, v1, v0 Functional tests without mask, vd = vs0
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst for load source vector
 * @eqm       macro for compare two vectors
 */
#define TEST_VCOMPRESS_VM_DEST_EQ_SRC0_INTERNAL(testnum, inst, result, vs1, vlen, mask, ebits, ldins, stins, eqm) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    COPY(RS1_ADDR, vs1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, mask, vlen, lh, sh, 2); \
    la a1, RS1_ADDR ; \
    la a3, RD_ADDR ; \
    la a4, MASK_ADDR ; \
    \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    ldins v0, (a4) ; \
    sub a0, a0, t0; \
    inst v0, v1, v0; \
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
 * vcompress.vm v1, v1, v0 Functional tests with mask, vd = vs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @vs1      start addr for source vector
 * @vlen      vector length
 * @mask      start addr for mask vector
 */
#define TEST_VCOMPRESS_VM_DEST_EQ_SRC0_HF(testnum, result, vs1, vlen, mask) \
  TEST_VCOMPRESS_VM_DEST_EQ_SRC0_INTERNAL(testnum, vcompress.vm, result, vs1, vlen, mask, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#endif // __TEST_MACROS_VCOMPRESS_VM_H
