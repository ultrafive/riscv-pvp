// See LICENSE for license details.

#ifndef __TEST_MACROS_VELUT_M_H
#define __TEST_MACROS_VELUT_M_H

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

// As there are 16 bit in a float 16, the maxmial value of binary
// representation for a half float is 64*1024 - 1, the maximal index
// for LUT is 64*1024*2, so the maximal table size is 128kB.
// split L1B(last 1 buffer) into 3 blocks of the following size
// 576kB + 576kB + 128kB
#define VELUTM_RD_ADDR  0xc0000000
#define VELUTM_RS1_ADDR  0xc0090000
#define VELUTM_RS2_ADDR  0xC0120000
// The instruction set specification Rev0.19 has the following note:
// The address of table, the second source operand of lut.m,  must not
// be met the following conditions: 0x0F800 <= base_address < 0x2F7FF
// Now spike and hardware implementation both not compily with this.
// If the rule is compilied with later, the macro should be defined as
// follows:
// #define LUTM_RS2_ADDR 0x0F800

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.0001, 5)

/*******************************************************************************
 * Functional tests with basic data
 ******************************************************************************/

/**
 * Functional tests with basic data
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source matrix
 * @val2      start addr for source table
 * @width     matrix width
 * @height    matrix height
 * @tsize     size of the source table
 * @ebits     element bits, 8 for byte, 16 for half, 32 for word
 * @eqm       macro for compare two matrix
 */
#define TEST_VELUT_M_INTERNAL( testnum, result, val1, width, height, val2, tsize, ebits, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(VELUTM_RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  COPY(VELUTM_RS2_ADDR, val2, tsize, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0, 0, 0) \
  PERF_BEGIN() \
  la a0, VELUTM_RD_ADDR; \
  la a1, VELUTM_RS1_ADDR; \
  la a2, VELUTM_RS2_ADDR; \
  velut.m (a0), (a1), (a2); \
  PERF_END(width ## _ ## height ## _  ## testnum) \
  COPY(test_##testnum##_data, VELUTM_RD_ADDR, height*width, LDINS, STINS, ESIZE) \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

/**
 * Functional tests with basic data
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @tsize     size of the source table
 */
#define TEST_VELUT_M( testnum, width, height, tsize ) \
  TEST_VELUT_M_INTERNAL(testnum, t##testnum##_rd, t##testnum##_rs1, \
                        width, height, t##testnum##_rs2, tsize, 16, EQM)

/**
 * Functional tests with stride data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix
 * @width     matrix width
 * @height    matrix height
 * @val2      start addr for table
 * @tsize     size of the source table
 * @dstride   dest matrix stride
 * @sstride   source matrix stride
 * @eqm       macro for compare two matrix
 */
#define TEST_VELUT_M_STRIDE_INTERNAL(testnum, inst, result, val1, width, height, val2, tsize, dstride, sstride) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY_STRIDE_D(VELUTM_RS1_ADDR, val1, height, width, sstride, LDINS, STINS, ESIZE) \
  COPY(VELUTM_RS2_ADDR, val2, tsize, LDINS, STINS, ESIZE) \
  SETCSR(height, width, sstride, 0, dstride) \
  PERF_BEGIN() \
  la a0, VELUTM_RD_ADDR; \
  la a1, VELUTM_RS1_ADDR; \
  la a2, VELUTM_RS2_ADDR; \
  inst (a0), (a1), (a2); \
  PERF_END(width ## _ ## height ## _ ## sstride ## _ ##testnum) \
  COPY_STRIDE_S(test_##testnum##_data, VELUTM_RD_ADDR, height, width, dstride, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/**
 * Functional tests with stride data
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @tsize     size of the source table
 * @dstride   dest matrix stride
 * @sstride   source matrix stride
 */
#define TEST_VELUT_M_STRIDE( testnum, width, height, tsize, dstride, sstride) \
  TEST_VELUT_M_STRIDE_INTERNAL(testnum, velut.m, t##testnum##_rd, t##testnum##_rs1, width, height, t##testnum##_rs2, tsize, dstride, sstride)


/**
 * Functional tests with inplace compute on rs1
 *   rd = rs1
 *
 * @testnum   test case number
 * @result    start addr for test result
 * @val1      start addr for source matrix1
 * @width     matrix width
 * @height    matrix height
 * @val2      start addr for source matrix2
 * @tsize     size of the source table
 */
#define TEST_VELUT_M_INPLACE_RS1_INTERNAL( testnum, result, val1, width, height, val2, tsize) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(VELUTM_RS1_ADDR, val1, height*width, LDINS, STINS, ESIZE) \
  COPY(VELUTM_RS2_ADDR, val2, tsize, LDINS, STINS, ESIZE) \
  SETCSR(height, width, 0, 0, 0) \
  la a1, VELUTM_RS1_ADDR; \
  la a2, VELUTM_RS2_ADDR; \
  velut.m (a1), (a1), (a2); \
  COPY(test_##testnum##_data, VELUTM_RS1_ADDR, height*width, LDINS, STINS, ESIZE) \
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
 * @tsize     size of the source table
 */
#define TEST_VELUT_M_INPLACE_RS1( testnum, width, height, tsize) \
  TEST_VELUT_M_INPLACE_RS1_INTERNAL(testnum, t##testnum##_rd, \
                t##testnum##_rs1, width, height, t##testnum##_rs2, tsize )

/*******************************************************************************
 * Exception tests
 ******************************************************************************/

/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @doff      address offset for dest operand
 * @soff1     address offset for source operand 1
 * @soff2     address offset for source operand 2
 */
#define TEST_VELUT_M_MISALIGNED_BASE( testnum, width, height, doff, soff1, soff2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, VELUTM_RD_ADDR + doff; \
  li a1, VELUTM_RS1_ADDR + soff1; \
  li a2, VELUTM_RS2_ADDR + soff2; \
  velut.m (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Invalid params exception
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @tsize     size of the source table
 */
#define TEST_VELUT_M_INVALID_PARAM( testnum, width, height) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, VELUTM_RD_ADDR; \
  li a1, VELUTM_RS1_ADDR; \
  li a2, VELUTM_RS2_ADDR; \
  velut.m (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Misaligned address because stride for operands
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @dstride   stride for dest operand
 * @sstride  stride for source operand 1
 */
#define TEST_VELUT_M_MISALIGNED_STRIDE( testnum, width, height, dstride, sstride) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, sstride, 0, dstride) \
  li a0, VELUTM_RD_ADDR; \
  li a1, VELUTM_RS1_ADDR; \
  li a2, VELUTM_RS2_ADDR; \
  velut.m (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault
 *
 * @testnum   test case number
 * @width     matrix width
 * @height    matrix height
 * @src1      address for source operand 1
 * @src2      address for source operand 2
 */
#define TEST_VELUT_M_ACCESS_FAULT( testnum, width, height, dst, src1, src2) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, 0, 0) \
  li a0, dst; \
  li a1, src1; \
  li a2, src2; \
  velut.m (a0), (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

#endif
