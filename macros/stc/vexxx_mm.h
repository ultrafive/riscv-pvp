// See LICENSE for license details.

#ifndef __TEST_MACROS_VEXXX_MM_H
#define __TEST_MACROS_VEXXX_MM_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#define LDINS lh
#define STINS sh
#define ESIZE 2

#define SETCSR(height, width, stride_s1, stride_s2, stride_dst) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  li a0, (stride_s2 << 16 + stride_s1); \
  li a1, stride_dst; \
  csrw stride_s, a0; \
  csrw stride_d, a1;

#undef RD_ADDR
#undef RS1_ADDR
#undef RS2_ADDR
// split l1buffer into 3 blocks of same size
#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc006aaaa
#define RS2_ADDR  0xc00d5554

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.0001, 5)

/*******************************************************************************
 * Functional tests with basic data
 ******************************************************************************/

/**
 * Functional tests with basic data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @val2      start addr for source matrix2
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INTERNAL( testnum, inst, result, val1, val2, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  COPY(RS2_ADDR, val2, height*width, LDINS, STINS, ESIZE) \
  fence; \
  SETCSR(height, width, 0, 0, 0) \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  inst (a0), (a1), (a2); \
  PERF_END(width ## _ ## height) \
  fence; \
  COPY(test_##testnum##_data, RD_ADDR, height*width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with basic data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM( testnum, inst, width, height ) \
  TEST_VEXXX_MM_INTERNAL(testnum, inst, t##testnum##_rd, t##testnum##_rs1, t##testnum##_rs2, width, height)

/**
 * Functional tests with stride data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @val2      start addr for source matrix2
 * @width     matrix width
 * @height    matrix height
 * @dstride   dest matrix stride
 * @sstride1  source matrix 1 stride
 * @sstride2  source matrix 2 stride
 * @eqm       macro for compare two matrix
 */
#define TEST_VEXXX_MM_STRIDE_INTERNAL(testnum, inst, result, val1, val2, width, height, dstride, sstride1, sstride2) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_STRIDE_D(RS1_ADDR, val1, height, width, sstride1, LDINS, STINS, ESIZE) \
  COPY_STRIDE_D(RS2_ADDR, val2, height, width, sstride2, LDINS, STINS, ESIZE) \
  SETCSR(height, width, sstride1, sstride2, dstride) \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  inst (a0), (a1), (a2); \
  PERF_END(width ## _ ## height ## _ ## sstride1 ## _ ## sstride2 ## testnum) \
  COPY_STRIDE_S(test_##testnum##_data, RD_ADDR, height, width, dstride, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with stride data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dstride   dest matrix stride
 * @sstride1  source matrix 1 stride
 * @sstride2  source matrix 2 stride
 */
#define TEST_VEXXX_MM_STRIDE( testnum, inst, width, height, dstride, sstride1, sstride2 ) \
  TEST_VEXXX_MM_STRIDE_INTERNAL(testnum, inst, t##testnum##_rd, t##testnum##_rs1, t##testnum##_rs2, width, height, dstride, sstride1, sstride2)


/**
 * Functional tests with inplace compute on rs1
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @val2      start addr for source matrix2
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS1_INTERNAL( testnum, inst, result, val1, val2, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  COPY(RS2_ADDR, val2, height*width, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0, 0, 0) \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  inst (a1), (a1), (a2); \
  COPY(test_##testnum##_data, RS1_ADDR, height*width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with inplace compute on rs1
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS1( testnum, inst, width, height ) \
  TEST_VEXXX_MM_INPLACE_RS1_INTERNAL(testnum, inst, \
      t##testnum##_rd, t##testnum##_rs1, t##testnum##_rs2, width, height )

/**
 * Functional tests with inplace compute on rs1
 *   rd = rs2
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @val2      start addr for source matrix2
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS2_INTERNAL( testnum, inst, result, val1, val2, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  COPY(RS2_ADDR, val2, height*width, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0, 0, 0) \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  inst (a2), (a1), (a2); \
  COPY(test_##testnum##_data, RS2_ADDR, height*width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with inplace compute on rs1
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS2( testnum, inst, width, height ) \
  TEST_VEXXX_MM_INPLACE_RS2_INTERNAL(testnum, inst, \
      t##testnum##_rd, t##testnum##_rs1, t##testnum##_rs2, width, height )

/**
 * Functional tests with inplace compute on rs1=rs2
 *   rd = rs1 = rs2
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS1_EQ_RS2_INTERNAL( testnum, inst, result, val1, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0, 0, 0) \
  la a0, RS1_ADDR; \
  inst (a0), (a0), (a0); \
  COPY(test_##testnum##_data, RS1_ADDR, height*width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with inplace compute on rs1
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INPLACE_RS1_EQ_RS2( testnum, inst, width, height ) \
  TEST_VEXXX_MM_INPLACE_RS1_EQ_RS2_INTERNAL(testnum, inst, \
      t##testnum##_rd, t##testnum##_rs1, width, height )

/*******************************************************************************
 * Exception tests
 ******************************************************************************/

/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @doff      address offset for dest operand
 * @soff1     address offset for source operand 1
 * @soff2     address offset for source operand 2
 */
#define TEST_VEXXX_MM_MISALIGNED_BASE( testnum, inst, width, height, doff, soff1, soff2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, RD_ADDR + doff; \
  li a1, RS1_ADDR + soff1; \
  li a2, RS2_ADDR + soff2; \
  inst (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Invalid params exception
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MM_INVALID_PARAM( testnum, inst, width, height) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  inst (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Misaligned address because stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dstride   stride for dest operand
 * @sstride1  stride for source operand 1
 * @sstride2  stride for source operand 2
 */
#define TEST_VEXXX_MM_MISALIGNED_STRIDE( testnum, inst, width, height, dstride, sstride1, sstride2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, dstride, sstride1, sstride2) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  inst (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dst       address for dest operand
 * @src1      address for source operand 1
 * @src2      address for source operand 2
 */
#define TEST_VEXXX_MM_ACCESS_FAULT( testnum, inst, width, height, dst, src1, src2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, dst; \
  li a1, src1; \
  li a2, src2; \
  inst (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

#endif
