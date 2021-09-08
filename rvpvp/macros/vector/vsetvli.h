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
 *    vsetvli rd, rs1, vtypei
 *    # rd = new vl, rs1 = AVL, vtypei = new vtype setting
 *
 * Authors: Xin Ouyang
 */
#ifndef __TEST_MACROS_VSETVLI_H
#define __TEST_MACROS_VSETVLI_H

#include "test_macros_v.h"

/*******************************************************************************
 * Functional tests
 ******************************************************************************/

/**
 * Functional tests
 *
 * @testnum   test case number
 * @result_vl     result value of vl
 * @result_vtype  result value of vtype
 * @val1      source register 1
 * @val2      source register 2
 */
#define TEST_VSETVLI( testnum, result_vl, result_vtype, val1, val2... ) \
test_ ## testnum: \
    li  TESTNUM, testnum; \
    li  x1, MASK_XLEN(val1); \
    PERF_BEGIN() \
    vsetvli x14, x1, val2; \
    PERF_END(testnum ## _ ## vlen) \
    \
    li  x7, MASK_XLEN(result_vl); \
    bne x14, x7, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    csrr t1, vl; \
    bne t1, x7, tofail_ ## testnum; \
    li  x7, MASK_XLEN(result_vtype); \
    csrr x8, vtype; \
    bne x8, x7, tofail_ ## testnum; \

/**
 * Functional tests with rs1 set to zero
 *
 * @testnum   test case number
 * @result_vl     result value of vl
 * @result_vtype  result value of vtype
 * @val2      source register 2
 */
#define TEST_VSETVLI_SRC1_ZERO( testnum, result_vl, result_vtype, val2... ) \
test_ ## testnum: \
    li  TESTNUM, testnum; \
    vsetvli x14, x0, val2; \
    \
    li  x7, MASK_XLEN(result_vl); \
    bne x14, x7, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    csrr t1, vl; \
    bne t1, x7, tofail_ ## testnum; \
    li  x7, MASK_XLEN(result_vtype); \
    csrr x8, vtype; \
    bne x8, x7, tofail_ ## testnum; \


/**
 * Functional tests with rd set to zero
 *
 * @testnum   test case number
 * @result_vl     result value of vl
 * @result_vtype  result value of vtype
 * @val2      source register 2
 */
#define TEST_VSETVLI_DEST_ZERO( testnum, result_vl, result_vtype, val1, val2... ) \
test_ ## testnum: \
    li  TESTNUM, testnum; \
    li  x1, MASK_XLEN(val1); \
    vsetvli x0, x1, val2; \
    \
    li  x7, MASK_XLEN(result_vl); \
    csrr t1, vl; \
    bne t1, x7, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    li  x7, MASK_XLEN(result_vtype); \
    csrr x8, vtype; \
    bne x8, x7, tofail_ ## testnum; \

/**
 * Functional tests with rd and rs1 set to zero
 *
 * @testnum   test case number
 * @result_vl     result value of vl
 * @result_vtype  result value of vtype
 * @val2      source register 2
 */
#define TEST_VSETVLI_DEST_SRC1_ZERO( testnum, result_vl, result_vtype, val2... ) \
test_ ## testnum: \
    li  TESTNUM, testnum; \
    vsetvli x0, x0, val2; \
    \
    li  x7, MASK_XLEN(result_vl); \
    csrr t1, vl; \
    bne t1, x7, tofail_ ## testnum; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    li  x7, MASK_XLEN(result_vtype); \
    csrr x8, vtype; \
    bne x8, x7, tofail_ ## testnum; \

/**
 * Functional tests
 *
 * @testnum   test case number
 * @val1      source register 1
 * @val2      source register 2
 */
#define TEST_VSETVLI_VTYPE_INVALID( testnum, val1, val2... ) \
test_ ## testnum: \
    li  TESTNUM, testnum; \
    li  x1, MASK_XLEN(val1); \
    vsetvli x14, x1, val2; \
    \
    li  x7, (1 << (__riscv_xlen - 1)); \
    csrr x8, vtype; \
    j topass_ ## testnum; \
tofail_ ## testnum: \
    j fail; \
topass_ ## testnum: \
    bne x8, x7, tofail_ ## testnum; \

#endif // __TEST_MACROS_VSETVLI_H
