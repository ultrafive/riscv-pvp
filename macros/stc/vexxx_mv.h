// See LICENSE for license details.

#ifndef __TEST_MACROS_VEXXX_MV_H
#define __TEST_MACROS_VEXXX_MV_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#ifndef INST
#error INST must be defined
#endif

#undef RD_ADDR
#undef RS1_ADDR
#undef RS2_ADDR

#if defined(X32_MV)
// vexxx.x32.mv
#define CODE(inst, rd, rs1, rs2, dim)  inst (rd), (rs1), (rs2)

#define ESIZE_IN    4
#define LDINS_IN    lw
#define STINS_IN    sw
#define ESIZE_OUT   2
#define LDINS_OUT   lh
#define STINS_OUT   sh

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.001, 5)

// split L1 into 1 / 2 / 2
#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc0050000
#define RS2_ADDR  0xc00f0000

#else
// vexxx.mv
#define CODE(inst, rd, rs1, rs2, dim)  inst (rd), (rs1), (rs2), dim

#define ESIZE_IN    2
#define LDINS_IN    lh
#define STINS_IN    sh
#define ESIZE_OUT   2
#define LDINS_OUT   lh
#define STINS_OUT   sh

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.01, 5)

// split L1 into 1 / 1 / 1
#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc006aaa8
#define RS2_ADDR  0xc00d5554

#endif

#define COPY_IN(dst, src, len) COPY(dst, src, len, LDINS_IN, STINS_IN, ESIZE_IN)
#define COPY_OUT(dst, src, len) COPY(dst, src, len, LDINS_OUT, STINS_OUT, ESIZE_OUT)

#define COPY_IN_STRIDE(dst, src, h, w, stride) COPY_STRIDE_D(dst, src, h, w, stride, LDINS_IN, STINS_IN, ESIZE_IN)
#define COPY_OUT_STRIDE(dst, src, h, w, stride) COPY_STRIDE_S(dst, src, h, w, stride, LDINS_OUT, STINS_OUT, ESIZE_OUT)

#define SETCSR(height, width, stride_s1, stride_dst) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  li a0, (stride_s1); \
  li a1, stride_dst; \
  csrw stride_s, a0; \
  csrw stride_d, a1;

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
 * @val2      start addr for source vector2
 * @width     matrix width
 * @height    matrix height
 * @vlen      vector length
 * @dim       dim
 */
#define VEXXX_MV( testnum, inst, result, val1, val2, width, height, vlen, dim) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_IN(RS1_ADDR, val1, height*width) \
  COPY_IN(RS2_ADDR, val2, vlen) \
  SETCSR(height, width, 0, 0) \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  CODE(inst, a0, a1, a2, dim); \
  PERF_END(width ## _ ## height ## _ ## dim) \
  COPY_OUT(test_##testnum##_data, RD_ADDR, height*width) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE_OUT, 0; \
  .popsection


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
 * @vlen      vector length
 * @dim       dim
 * @dstride   dest matrix stride
 * @sstride1  source matrix 1 stride
 */
#define VEXXX_MV_STRIDE(testnum, inst, result, val1, val2, width, height, vlen, dim, dstride, sstride1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_IN_STRIDE(RS1_ADDR, val1, height, width, sstride1) \
  COPY_IN(RS2_ADDR, val2, vlen) \
  SETCSR(height, width, sstride1, dstride) \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  CODE(inst, a0, a1, a2, dim); \
  PERF_END(width ## _ ## height ## _ ## sstride1 ## _ ## testnum) \
  COPY_OUT_STRIDE(test_##testnum##_data, RD_ADDR, height, width, dstride) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE_OUT, 0; \
  .popsection


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
 * @vlen      vector length
 * @dim       dim
 */
#define VEXXX_MV_INPLACE_RS1( testnum, inst, result, val1, val2, width, height, vlen, dim) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_IN(RS1_ADDR, val1, height*width) \
  COPY_IN(RS2_ADDR, val2, vlen) \
  SETCSR(height, width, 0, 0) \
  la a1, RS1_ADDR; \
  la a2, RS2_ADDR; \
  CODE(inst, a0, a1, a2, dim); \
  COPY_OUT(test_##testnum##_data, RS1_ADDR, height*width) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE_OUT, 0; \
  .popsection

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
 * @dim       dim
 * @doff      address offset for dest operand
 * @soff1     address offset for source operand 1
 * @soff2     address offset for source operand 2
 */
#define VEXXX_MV_MISALIGNED_BASE( testnum, inst, width, height, dim, doff, soff1, soff2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0) \
  li a0, RD_ADDR + doff; \
  li a1, RS1_ADDR + soff1; \
  li a2, RS2_ADDR + soff2; \
  CODE(inst, a0, a1, a2, dim); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Invalid params exception
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dim       dim
 */
#define VEXXX_MV_INVALID_PARAM( testnum, inst, width, height, dim) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  CODE(inst, a0, a1, a2, dim); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Misaligned address because stride for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dim       dim
 * @dstride   stride for dest operand
 * @sstride1  stride for source operand 1
 */
#define VEXXX_MV_MISALIGNED_STRIDE( testnum, inst, width, height, dim, dstride, sstride1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, sstride1, dstride) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  CODE(inst, a0, a1, a2, dim); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dim       dim
 * @dst       address for dest operand
 * @src1      address for source operand 1
 * @src2      address for source operand 2
 */
#define VEXXX_MV_ACCESS_FAULT( testnum, inst, width, height, dim, dst, src1, src2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0) \
  li a0, dst; \
  li a1, src1; \
  li a2, src2; \
  CODE(inst, a0, a1, a2, dim); \
  j fail; \
test_ ## testnum ## _end: \


/*
  Public test case wrappers
*/
/**
 * Functional tests with basic data, dim_h
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MV_DIMH( num, width, height ) \
  VEXXX_MV(num, INST, t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, width, dim_h)

/**
 * Functional tests with basic data, dim_w
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MV_DIMW( num, width, height ) \
  VEXXX_MV(num, INST, t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, height, dim_w)

/**
 * Functional tests with stride data, dim_h
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dstride   dest matrix stride
 * @sstride1  source matrix 1 stride
 */
#define TEST_VEXXX_MV_DIMH_STRIDE( num, width, height, dstride, sstride1 ) \
  VEXXX_MV_STRIDE(num, INST, t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, width, dim_h, dstride, sstride1)


/**
 * Functional tests with stride data, dim_w
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @dstride   dest matrix stride
 * @sstride1  source matrix 1 stride
 */
#define TEST_VEXXX_MV_DIMW_STRIDE( num, width, height, dstride, sstride1 ) \
  VEXXX_MV_STRIDE(num, INST, t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, height, dim_w, dstride, sstride1)

/**
 * Functional tests with inplace compute on rs1, dim_h
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MV_DIMH_INPLACE_RS1( num, width, height ) \
  VEXXX_MV_INPLACE_RS1(num, INST, \
      t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, width, dim_h )

/**
 * Functional tests with inplace compute on rs1, dim_w
 *   rd = rs1
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 */
#define TEST_VEXXX_MV_DIMW_INPLACE_RS1( num, width, height ) \
  VEXXX_MV_INPLACE_RS1(num, INST, \
      t##num##_rd, t##num##_rs1, t##num##_vs2, width, height, height, dim_w )


#define TEST_VEXXX_MV_MISALIGNED_BASE(num, width, height, dim, doff, soff1, soff2) \
  VEXXX_MV_MISALIGNED_BASE(num, INST, width, height, dim, doff, soff1, soff2)

#define TEST_VEXXX_MV_MISALIGNED_STRIDE(num, width, height, dim, dstride, sstride1) \
  VEXXX_MV_MISALIGNED_STRIDE(num, INST, width, height, dim, dstride, sstride1)

#define TEST_VEXXX_MV_INVALID_PARAM(num, width, height, dim) \
  VEXXX_MV_INVALID_PARAM(num, INST, width, height, dim)

#define TEST_VEXXX_MV_ACCESS_FAULT(num, width, height, dim, result, val1, val2) \
  VEXXX_MV_ACCESS_FAULT(num, INST, width, height, dim, result, val1, val2)


#endif
