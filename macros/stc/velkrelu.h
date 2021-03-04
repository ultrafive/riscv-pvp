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
 * Tests for velkrelu.m* instructions
 *
 *    1) velkrelu.mf (rd), (rs1), rs2
 *         k = (fp16)rs2
 *         M[0, 0]=(rd), A[0, 0]=(rs1), T[0, 0] = temp
 *         tij = (aij > 0) ? 1: k
 *         M[i, j] = A[i, j] * T[i, j]
 *    2) velkrelu.mv (rd), (rs1), (rs2), dim_h
 *         velkrelu.mv (rd), (rs1), (rs2), dim_h
 *         M = (M1i > 0) ? (M1i: K * M1i)
 *         In detail:
 *           M[0, 0]=(rd), A[0, 0]=(rs1), T[0] = (rs2), Kt[0,0] = temp
 *           Kt[i, j] = A[i, j] > 0 ? 1 : T[j];
 *           M[i, j] = A[i, j] * Kt[i, j]
 *
 *    3) velkrelu.mv (rd), (rs1), (rs2), dim_w
 *
 * Authors: Liyong Zeng
 */
#ifndef __TEST_MACROS_VELKRELU_H
#define __TEST_MACROS_VELKRELU_H

#include "test_macros_stc.h"
#include "exception.h"
// Now the size of L1B of NCP is 1024kB+256kB
// from 0xC0000000 ~ 0xC013FFFF.
// To test velkrelu instruction to fetch source operand from L1B,
// the first source operand is copied to the starting address of L1B.
#define VELKRELU_RS1_ADDR 0xC0000000

// The starting address of dest operand. The maximal size of dest
// matrix is the same size as the source matrix.(512kB)
#define VELKRELU_RD_ADDR 0xC00A0000

// For instruction velkrelu.mv, there are a source matrix , a source
// vector and dest matrix. To fill the L1B fully, source matrix and
// dest matrix all be allocted 638kB, from 0xC0000000~0xC009F7FFF,
// and the source vector will be allocted 2kB(1024 number of float16).
// the second source operand is copied to the starting address of 0xC0080000
// to 0xC00BFFF
#define VELKRELU_RS2_ADDR 0xC009F800

// The starting address of dest operand for velkrelu.mv . The maximal size of
// dest matrix is the same size as the source matrix(638kB), from 0xC00A0000
// to 0xC013FFFF
#define VELKRELU_MV_RD_ADDR 0xC00A0000


// The absolute torlance, for float16, the atol is 1e0-4
#define VELKRELU_ATOL 0.001
// The relative torlance as binary comparsion for two float16 number
#define VELKRELU_RTOL 2

#define MOVE_TO_L1B_AS_HF(l1b_addr, src_addr, size) \
  COPY(l1b_addr, src_addr, size, lh, sh, 2); \

#define WRITE_RESULT_AS_HF(testnum, result, size) \
  COPY(test_ ## testnum ## _data, result, size, lh, sh, 2); \

#define EQM(result, golden_data, size) \
  VV_CHECK_EQ_HF_DEFAULT(result, golden_data, size); \


/* Set shapes and strides */
#define SETCSR(height_s1, width_s1, stride_s1, stride_res) \
  li a0, (width_s1 << 16 + height_s1); \
  csrw shape_s1, a0; \
  li a0, (stride_s1 & 0xffff); \
  csrw stride_s, a0; \
  li a0, (stride_res & 0xffff); \
  csrw stride_d, a0; \

/*******************************************************************************
 * Functional tests
 ******************************************************************************/

/**
 * Functional tests
 *
 * @testnum    test case number
 * @res_matrix result matrix
 * @src_matrix source matrix
 * @width      width of source matrix
 * @height     height of source matrix
 * @src_float  source floating number
 */
#define TEST_VELKRELU_MF_INTERNAL( testnum, res_matrix, src_matrix, src_float, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  la a2, src_float; \
  flw fa0, 0(a2); \
  PERF_BEGIN() \
  li a2, VELKRELU_RD_ADDR; \
  li a3, VELKRELU_RS1_ADDR; \
  velkrelu.mf (a2), (a3), fa0; \
  PERF_END(width ## _ ## height ## _ ## testnum) \
  la a4, test_ ## testnum ## _data; \
  WRITE_RESULT_AS_HF(testnum, VELKRELU_RD_ADDR, width*height); \
  EQM(res_matrix, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection

#define TEST_VELKRELU_MF(testnum, width, height) \
         TEST_VELKRELU_MF_INTERNAL(testnum, t ## testnum ## _rd, t ## testnum ## _rs1, t ## testnum ## _rs2, width, height) \

/*******************************************************************************
 * Abnormal input tests
 ******************************************************************************/

/**
 * Computation in place rs1
 * When the following conditions are met, computation can be placed in rs1.
 * That is res_matrix = src_matrix.
 *  1) stride of source matrix >= stride of result matrix
 *  2) stride of source matrix >= length of row of source matrix
 *  3) stride of result matrix >= lenght of row of source matrix
 * @testnum    test case number
 * @res_matrix result matrix
 * @src_matrix source matrix
 * @width      width of source matrix
 * @height     height of source matrix
 * @src_float  source floating number
 */
#define TEST_VELKRELU_MF_INPLACE_SRC1_INTERNAL( testnum, res_matrix, src_matrix, src_float, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  la a2, src_float; \
  flw fa0, 0(a2); \
  li a3, VELKRELU_RS1_ADDR; \
  velkrelu.mf (a3), (a3), fa0; \
  WRITE_RESULT_AS_HF(testnum, VELKRELU_RS1_ADDR, width*height); \
  EQM(res_matrix, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection

#define TEST_VELKRELU_MF_INPLACE_SRC1(testnum, width, height) \
        TEST_VELKRELU_MF_INPLACE_SRC1_INTERNAL(testnum, t ## testnum ## _rd, t ## testnum ## _rs1, t ## testnum ## _rs2, width, height) \
/**
 * Test velkrelu.mf with address of misaligned offset 'offset'
 * in the source matrix operand.
 */
#define TEST_VELKRELU_MF_MISALIGNED_LOAD_INTERNAL( testnum, res_matrix, src_matrix, src_float, width, height, offset) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
    li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
    la a2, src_float; \
    flw fa0, 0(a2); \
    li a2, VELKRELU_RD_ADDR; \
    li a3, VELKRELU_RS1_ADDR+offset; \
  velkrelu.mf (a2), (a3), fa0; \
    j fail; \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection \
test_ ## testnum ## _end: \

#define TEST_VELKRELU_MF_MISALIGNED_LOAD(testnum, width, height, offset) \
        TEST_VELKRELU_MF_MISALIGNED_LOAD_INTERNAL( testnum, t ## testnum ## _rd, t ## testnum ## _rs1, t ## testnum ## _rs2, width, height, offset) \
/**
 * Test velkrelu.mf with address of misaligned offset 'offset' in
 * the dest operands.
 */
#define TEST_VELKRELU_MF_MISALIGNED_STORE_INTERNAL( testnum, res_matrix, src_matrix, src_float, width, height, offset) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
    li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
    la a2, src_float; \
    flw fa0, 0(a2); \
    li a2, VELKRELU_RD_ADDR+offset; \
    li a3, VELKRELU_RS1_ADDR; \
  velkrelu.mf (a2), (a3), fa0; \
    j fail; \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection \
test_ ## testnum ## _end: \

#define TEST_VELKRELU_MF_MISALIGNED_STORE(testnum, width, height, offset) \
        TEST_VELKRELU_MF_MISALIGNED_STORE_INTERNAL( testnum, t ## testnum ## _rd, t ## testnum ## _rs1, t ## testnum ## _rs2, width, height, offset) \

// Test for instruction velkrelu.mv
/*******************************************************************************
 * Functional tests
 ******************************************************************************/

/**
 * Functional tests
 *
 * @testnum    test case number
 * @res_matrix result matrix
 * @src_matrix source matrix
 * @src_vec    source vector
 * @height     height of source matrix
 * @width      width of source matrix
 * @vlen       length of source vector
 * @dim_flag   dimention flag, dim_h or dim_w
 */
#define TEST_VELKRELU_MV_INTERNAL(testnum, res_matrix, src_matrix, src_vec, \
                                  height, width, vlen, dim_flag) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  SETCSR(height, width, (width*2), (width*2)); \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
  li a2, VELKRELU_MV_RD_ADDR; \
  li a3, VELKRELU_RS1_ADDR; \
  li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
  WRITE_RESULT_AS_HF(testnum, VELKRELU_MV_RD_ADDR, width*height); \
  EQM(res_matrix, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection

// #define TEST_VELKRELU_MV(testnum, height, width, vlen, dim_flag) \
//          TEST_VELKRELU_MV_INTERNAL(testnum, t ## testnum ## _rd, \
//            t ## testnum ## _rs1, t ## testnum ## _rs2, height, width, \
//            vlen, dim_flag) \
//
/**
 * Functional tests with stride
 *
 * @testnum    test case number
 * @res_matrix result matrix
 * @src_matrix source matrix
 * @src_vec    source vector
 * @height     height of source matrix
 * @width      width of source matrix
 * @vlen       length of source vector
 * @dim_flag   dimention flag, dim_h or dim_w
 */
#define TEST_VELKRELU_MV_STRIDED_INTERNAL(testnum, res_matrix, src_matrix, src_vec, \
                                  height, width, vlen, stride_s, stride_d, dim_flag) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_STRIDE_D(VELKRELU_RS1_ADDR, src_matrix, height, width, stride_s, lh, sh, 2); \
  SETCSR(height, width, stride_s, stride_d); \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
  PERF_BEGIN() \
  li a2, VELKRELU_MV_RD_ADDR; \
  li a3, VELKRELU_RS1_ADDR; \
  li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
  PERF_END(width ## _ ## height ## _ ## stride_s ## _ ## testnum) \
  COPY_STRIDE_S(test_ ## testnum ## _data, VELKRELU_MV_RD_ADDR, height, width, stride_d, lh, sh, 2); \
  EQM(res_matrix, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection

/*******************************************************************************
 * Abnormal input tests
 ******************************************************************************/

/**
 * Computation in place rs1
 * When the following conditions are met, computation can be placed in rs1.
 * That is res_matrix = src_matrix.
 *  1) stride of source matrix >= stride of result matrix
 *  2) stride of source matrix >= length of row of source matrix
 *  3) stride of result matrix >= lenght of row of source matrix
 */
/**
 * Functional tests
 *
 * @testnum    test case number
 * @res_matrix result matrix
 * @src_matrix source matrix
 * @src_vec    source vector
 * @width      width of source matrix
 * @height     height of source matrix
 * @vlen       length of source vector
 * @dim_flag   dimention flag, dim_h or dim_w
 */
#define TEST_VELKRELU_MV_INPLACE_SRC1_INTERNAL(testnum, res_matrix, src_matrix,\
          src_vec, height, width, vlen, dim_flag) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  SETCSR(height, width, (width*2), (width*2)); \
  MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
  li a3, VELKRELU_RS1_ADDR; \
  li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a3), (a3), (a4), dim_flag; \
  WRITE_RESULT_AS_HF(testnum, VELKRELU_RS1_ADDR, width*height); \
  EQM(res_matrix, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection

#define TEST_VELKRELU_MV_INPLACE_SRC1(testnum, height, width, vlen, dim_flag) \
         TEST_VELKRELU_MV_INPLACE_SRC1_INTERNAL(testnum, t ## testnum ## _rd, \
           t ## testnum ## _rs1, t ## testnum ## _rs2, width, \
             height, vlen, dim_flag) \

/**
 * Test velkrelu.mv with address of misaligned offset 'offset'
 * in the source matrix operand.
 */
#define TEST_VELKRELU_MV_MISALIGNED_LOAD_INTERNAL(testnum, res_matrix, src_matrix, src_vec, height, width, vlen, offset, dim_flag) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  SETCSR(height, width, (width*2), (width*2)); \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
    li a2, VELKRELU_MV_RD_ADDR; \
    li a3, (VELKRELU_RS1_ADDR+offset); \
    li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
    j fail; \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection \
test_ ## testnum ## _end: \

#define TEST_VELKRELU_MV_MISALIGNED_LOAD(testnum, height, width, vlen, offset, dim_flag) \
         TEST_VELKRELU_MV_MISALIGNED_LOAD_INTERNAL(testnum, \
            t ## testnum ## _rd, \
            t ## testnum ## _rs1, \
            t ## testnum ## _rs2, \
            width,\
            height, \
            vlen, \
            offset, \
            dim_flag) \
/**
 * Test velkrelu.mv with address of misaligned offset 'offset' in
 * the dest operands.
 */
#define TEST_VELKRELU_MV_MISALIGNED_STORE_INTERNAL(testnum, res_matrix, src_matrix, src_vec, height, width, vlen, offset, dim_flag) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, width*height); \
  SETCSR(height, width, (width*2), (width*2)); \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
    li a2, VELKRELU_MV_RD_ADDR+offset; \
    li a3, VELKRELU_RS1_ADDR; \
    li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
    j fail; \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), 2, 0; \
  .popsection \
test_ ## testnum ## _end: \

#define TEST_VELKRELU_MV_MISALIGNED_STORE(testnum, height, width, vlen, \
                                          offset, dim_flag) \
        TEST_VELKRELU_MV_MISALIGNED_STORE_INTERNAL(testnum, \
          t ## testnum ## _rd, \
          t ## testnum ## _rs1,\
          t ## testnum ## _rs2,\
          height,\
          width,\
          vlen,\
          offset, \
          dim_flag) \

/**
 * Test velkrelu.mv with address of out of limit of L1B or IM buffer.
 */
#define TEST_VELKRELU_MV_OUTOF_LIMIT(testnum, rd_addr, src1_addr, \
                                     src2_addr, height, width, vlen, dim_flag) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
  SETCSR(height, width, (width*2), (width*2)); \
    li a2, rd_addr; \
    li a3, src1_addr; \
    li a4, src2_addr; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
    j fail; \
test_ ## testnum ## _end: \

#define TEST_VELKRELU_MV_MISALIGNED_STRIDE_INTERNAL(testnum, res_matrix, \
                                                 src_matrix, src_vec, \
                                                 height, width,\
                                                 vlen, stride_s, \
                                                 stride_d, dim_flag) \
test_ ## testnum: \
    TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
    li TESTNUM, testnum; \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS1_ADDR, src_matrix, (height*width)); \
  SETCSR(height, width, stride_s, stride_d); \
    MOVE_TO_L1B_AS_HF(VELKRELU_RS2_ADDR, src_vec, vlen); \
    li a2, VELKRELU_MV_RD_ADDR; \
    li a3, VELKRELU_RS1_ADDR; \
    li a4, VELKRELU_RS2_ADDR; \
  velkrelu.mv (a2), (a3), (a4), dim_flag; \
    j fail; \
test_ ## testnum ## _end: \

#endif // __TEST_MACROS_VELKRELU_H
