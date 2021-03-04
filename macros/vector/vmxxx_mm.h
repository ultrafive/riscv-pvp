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
 * Tests for vfxxx.vv instructions
 * 
 *    vmxxx.mm vd, vs2, vs1
 * 
 * Authors: Hao Chen
 */
#ifndef __TEST_MACROS_VMXXX_MM_H
#define __TEST_MACROS_VMXXX_MM_H

#include "vfxxx_vv.h"

/**
 * vmxxx.mm vd, vs2, vs1 SH Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VMXXX_MM_SH(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VV_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vmxxx.mm vd, vs1, vs1 SH Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 */
#define TEST_VMXXX_MM_SRC2_EQ_SRC1_SH(testnum, inst, result, val1, vlen) \
  TEST_VFXXX_VV_SRC2_EQ_SRC1_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vmxxx.mm vs1, vs1, vs1 SH Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @vlen      vector length
 */
#define TEST_VMXXX_MM_DEST_EQ_SRC12_SH(testnum, inst, result, val1, vlen) \
  TEST_VFXXX_VV_DEST_EQ_SRC12_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vmxxx.mm vs1, vs2, vs1 SH Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VMXXX_MM_DEST_EQ_SRC1_SH(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VV_DEST_EQ_SRC1_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

/**
 * vmxxx.mm vs2, vs2, vs1 SH Functional tests
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source vector 1
 * @val2      start addr for source vector 2
 * @vlen      vector length
 */
#define TEST_VMXXX_MM_DEST_EQ_SRC2_SH(testnum, inst, result, val1, val2, vlen) \
  TEST_VFXXX_VV_DEST_EQ_SRC2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#endif // __TEST_MACROS_VFXXX_VV_H
