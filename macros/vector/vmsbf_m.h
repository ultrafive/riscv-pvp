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
 * Tests for vmsbf.m instructions
 * 
 *    vmsbf.m vd, vs2, vm
 * 
 * Authors: Li Zhiyong
 */
#ifndef __TEST_MACROS_VMSBF_M_H
#define __TEST_MACROS_VMSBF_M_H

#include "test_macros_v.h"
#include "test_macros.h"
#include "vmsxf_m.h"

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_MSBF_M_HF(testnum, result, val1, vlen) \
TEST_V_VMSXF_M_HF(testnum, vmsbf.m, result, val1, vlen)


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_MSBF_M_DEST_EQU_SRC_HF(testnum, result, val1, vlen) \
TEST_V_VMSXF_M_DEST_EQU_SRC_HF(testnum, vmsbf.m, result, val1, vlen)


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr to save the result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_MSBF_M_MASK_HF(testnum, result, vd, val1, val0, vlen) \
TEST_V_MSXF_M_MASK_HF(testnum, vmsbf.m, result, vd, val1, vlen, val0)

/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr to save result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_MSBF_M_MASK_VS2_EQU_V0T_HF(testnum, result, vd, val0, vlen) \
TEST_V_MSXF_M_MASK_VS2_EQU_V0T_HF(testnum, vmsbf.m, result, vd, vlen, val0)


/**
 * Functional tests without mask
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @vd        start addr to save result
 * @val1      start addr for source vector1
 * @vlen      vector length
 */
#define TEST_V_MSBF_M_MASK_VD_EQU_VS2_EQU_V0T_HF(testnum, result, vd, val0, vlen) \
TEST_V_MSXF_M_MASK_VD_EQU_VS2_EQU_V0T_HF(testnum, vmsbf.m, result, vd, vlen, val0)



#endif // __TEST_MACROS_VMSBF_M_H
