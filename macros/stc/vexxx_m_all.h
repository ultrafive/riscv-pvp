// See LICENSE for license details.

#ifndef __TEST_MACROS_VEXXX_M_ALL_H
#define __TEST_MACROS_VEXXX_M_ALL_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#define LDINS lh
#define STINS sh
#define ESIZE 2

#define SETCSR(height, width, stride_s1) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  li a0, (stride_s1); \
  csrw stride_s, a0;

#undef RD_ADDR
#undef RS1_ADDR
// split l1buffer into 2 blocks of same size
#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc00a0000

#ifndef FP_CHECK_EQ
#define FP_CHECK_EQ(fp0, fp1, acc) \
    feq.s a0, fp0, fp1; \
    bnez a0, 1f; \
    j fail; \
1:;
#endif

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
#define TEST_VEXXX_M_ALL_INTERNAL( testnum, inst, result, val1, width, height) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0) \
  PERF_BEGIN() \
  la a1, RS1_ADDR; \
  inst fa0, (a1); \
  PERF_END(width ## _ ## height ## _ ## testnum) \
  la a1, result; \
  flw fa1, 0(a1); \
  FP_CHECK_EQ(fa0, fa1, width * height); \

/**
 * Functional tests with basic data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_M_ALL( testnum, inst, width, height ) \
  TEST_VEXXX_M_ALL_INTERNAL(testnum, inst, t##testnum##_rd, t##testnum##_rs1, width, height)

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
#define TEST_VEXXX_M_ALL_STRIDE_INTERNAL(testnum, inst, result, val1, width, height, sstride1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_STRIDE_D(RS1_ADDR, val1, height, width, sstride1, LDINS, STINS, ESIZE) \
  SETCSR(height, width, sstride1) \
  PERF_BEGIN() \
  la a1, RS1_ADDR; \
  inst fa0, (a1); \
  PERF_END(width ## _ ## height ## _ ## sstride1 ## _ ## testnum) \
  la a1, result; \
  flw fa1, 0(a1); \
  FP_CHECK_EQ(fa0, fa1, width * height);

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
#define TEST_VEXXX_M_ALL_STRIDE( testnum, inst, width, height, sstride1 ) \
  TEST_VEXXX_M_ALL_STRIDE_INTERNAL(testnum, inst, t##testnum##_rd, t##testnum##_rs1, width, height, sstride1)

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
 * @soff1     address offset for source operand 1
 */
#define TEST_VEXXX_M_ALL_MISALIGNED_BASE( testnum, inst, width, height, soff1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0) \
  li a1, RS1_ADDR + soff1; \
  inst fa0, (a1); \
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
#define TEST_VEXXX_M_ALL_INVALID_PARAM( testnum, inst, width, height) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0) \
  li a1, RS1_ADDR; \
  inst fa0, (a1); \
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
#define TEST_VEXXX_M_ALL_MISALIGNED_STRIDE( testnum, inst, width, height, sstride1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, sstride1) \
  PERF_BEGIN() \
  li a1, RS1_ADDR; \
  inst fa0, (a1); \
  PERF_END(width ## _ ## height ## _ ## sstride1 ## _ ## testnum) \
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
#define TEST_VEXXX_M_ALL_ACCESS_FAULT( testnum, inst, width, height, src1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0) \
  li a1, src1; \
  inst fa0, (a1); \
  j fail; \
test_ ## testnum ## _end: \

#endif
