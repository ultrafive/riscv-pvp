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
 * Tests for viota.m instructions
 * 
 *    viota.m vd, vs2, vm
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VIOTA_M_H
#define __TEST_MACROS_VIOTA_M_H

#include "test_macros_v.h"
#include "test_macros.h"
#include "vmsxf_m.h"
#include "exception.h"


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_IOTA_M_HF(testnum, result, val1, vlen) \
TEST_V_VMSXF_M_HF(testnum, viota.m, result, val1, vlen)


/**
 * Functional tests with mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr to save the result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_IOTA_M_MASK_HF(testnum, result, vd, val1, val0, vlen) \
TEST_V_MSXF_M_MASK_HF(testnum, viota.m, result, vd, val1, vlen, val0)

/**
 * Functional tests with mask and vs2=vm
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr to save result
 * @val0      start addr for source vector vm(v0)
 * @vlen      vector length
 */
#define TEST_V_IOTA_M_MASK_VS2_EQU_V0T_HF(testnum, result, vd, val0, vlen) \
TEST_V_MSXF_M_MASK_VS2_EQU_V0T_HF(testnum, viota.m, result, vd, vlen, val0)


/**
 * Exception tests, vd=vs2
 *
 * @testnum   test case number
 * @val1      start addr for source vec1
 * @vlen      vector length
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 */
#define TEST_EXCPT_V_IOTA_M_DEST_EQU_SRC_INTERNAL(testnum, val1, vlen, ebits, ldins) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end);\
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, RS2_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  viota.m v1, v1 ; \
    j fail ;\
test_ ## testnum ## _end:


/**
 * Exception tests, vd=vs2
 *
 * @testnum   test case number
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_EXCPT_V_IOTA_M_DEST_EQU_SRC_HF(testnum, val1, vlen) \
  TEST_EXCPT_V_IOTA_M_DEST_EQU_SRC_INTERNAL(testnum, val1, vlen, 16, vlh.v)


/**
 * Exception tests, vd=vm
 *
 * @testnum   test case number
 * @val1      start addr for source vec1
 * @vlen      vector length
 * @val0      start addr for vm vecotor(v0)
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @ldins     inst to load source vector
 * @stins     inst to store vector
 */
#define TEST_EXCPT_V_IOTA_M_DEST_EQU_VM_INTERNAL(testnum, val1, vlen, val0, ebits, ldins, stins) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_RVV_INVALID_SAME_RDRS, test_ ## testnum ## _end);\
    COPY(RS2_ADDR, val1, vlen, lh, sh, 2); \
    COPY(MASK_ADDR, val1, vlen, lh, sh, 2); \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, MASK_ADDR ; \
    la a2, RS2_ADDR ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a1); \
  ldins v1, (a2); \
  viota.m v0, v1, v0.t; \
    j fail ;\
test_ ## testnum ## _end:


/**
 * Exception tests, vd=vm
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_EXCPT_V_IOTA_M_DEST_EQU_VM_HF(testnum, val1, val0, vlen) \
    TEST_EXCPT_V_IOTA_M_DEST_EQU_VM_INTERNAL(testnum, val1, vlen, val0, 16, vlh.v, vsh.v)


#endif // __TEST_MACROS_VIOTA_M_H
