// See LICENSE for license details.

#ifndef __TEST_MACROS_MOVE_COMMON_H
#define __TEST_MACROS_MOVE_COMMON_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#define LDINS lh
#define STINS sh
#define ESIZE 2

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF_DEFAULT(vec1, vec2, vlen)

/*******************************************************************************
 * Template for functional testing with basic data
 ******************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       1) SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, sstride, dstride)
 *****************************************************************************/
/**
 * Template for functional testing to move matrix with basic data
 *
 * @testnum      test case number
 * @inst         inst to test
 * @result       start addr for test result
 * @val          start addr for source matrix
 * @width        matrix width
 * @height       matrix height
 * @dstride      stride of result matrix
 * @sstride      stride of source matrix
 * @dest_addr    address to save dest matrix
 * @src_addr     address to save source matrix
 */
#define TEST_MOVE_MAT_TEMPLATE( testnum, inst, result, val, width, height, \
                                dstride, sstride, dest_addr, src_addr) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  SETCSR(height, width, sstride, dstride) \
  COPY_STRIDE_D(src_addr, val, height, width, sstride, LDINS, STINS, ESIZE) \
  PERF_BEGIN() \
  la a0, src_addr; \
  la a1, dest_addr; \
  inst (a1), (a0); \
  PERF_END(width ## _ ## height ## _ ## testnum) \
  COPY_STRIDE_S(test_##testnum##_data, dest_addr, height, width, dstride, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection


/*******************************************************************************
 * Template for functional testing with specified exception
 ******************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       1) SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, sstride, dstride)
 *****************************************************************************/
/**
 * Template for functional testing to move matrix with specified exception
 *
 * @testnum      test case number
 * @inst         inst to test
 * @result       start addr for test result
 * @val          start addr for source matrix
 * @width        matrix width
 * @height       matrix height
 * @doff         offset of dest operand
 * @soff         offset of source operand
 * @dstride      stride of result matrix
 * @sstride      stride of source matrix
 * @dest_addr    address to save dest matrix
 * @src_addr     address to save source matrix
 * @exception    the specified exception to be tested
 */
#define TEST_MOVE_MAT_WITH_EXCEPTION_TEMPLATE( testnum, inst, result, val,  \
                                               width, height, doff, soff,   \
                                               dstride, sstride, dest_addr, \
                                               src_addr, exception) \
test_ ## testnum: \
  TEST_EXCEPTION(exception, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, sstride, dstride) \
  la a0, src_addr+soff; \
  la a1, dest_addr+doff; \
  inst (a1), (a0); \
  j fail; \
test_ ## testnum ## _end: \


/*******************************************************************************
 * Template for functional testing instructions to move vector and expand it to
 * a matrix based on the dim flag.
 *****************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, stride)
 *****************************************************************************/
/**
 * Template for functional testing with basic data
 *
 * @testnum  test case number
 * @inst     inst to test
 * @result   start addr for test result
 * @val      start addr for source matrix
 * @width    matrix width
 * @height   matrix height
 * @vlen     length of source vector
 * @stride   stride of result matrix
 * @src_addr address to place operand
 * @dest_addr address to place operand
 * @dim      direction flag string
 */
#define TEST_MOVE_VEC_TEMPLATE(testnum, inst, result, val, width, height, vlen, \
                               stride, src_addr, dest_addr, dim) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(src_addr, val, vlen, LDINS, STINS, ESIZE) \
  SETCSR(height, width, stride) \
  la a0, dest_addr; \
  la a1, src_addr; \
  inst (a0), (a1), dim; \
  COPY_STRIDE_S(test_##testnum##_data, dest_addr, height, width, stride, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, height*width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

/*******************************************************************************
 * Template for functional testing instructions to move vector and expand it to
 * a matrix based on the dim flag, the instruction will trigger the specified
 * exception.
 *****************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, 0, stride)
 *****************************************************************************/
/**
 * Template for functional testing with specified exception
 *
 * @testnum      test case number
 * @inst         inst to test
 * @result       start addr for test result
 * @val          start addr for source matrix
 * @width        width of result matrix
 * @height       height of result matrix
 * @vlen         length of vector
 * @doff         offset of dest operand
 * @soff         offset of source operand
 * @stride       stride of result matrix
 * @dest_addr    address to save dest matrix
 * @src_addr     address to save source matrix
 * @exception    the specified exception to be tested
 * @dim      direction flag string
 */
#define TEST_MOVE_VEC_WITH_EXCEPTION_TEMPLATE(testnum, inst, result, val, \
                                              width, height, vlen, doff, \
                                              soff, stride, dest_addr, \
                                              src_addr, exception, dim) \
test_ ## testnum: \
  TEST_EXCEPTION(exception, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, stride) \
  la a0, src_addr+soff; \
  la a1, dest_addr+doff; \
  inst (a1), (a0), dim; \
  j fail; \
test_ ## testnum ## _end: \

/*******************************************************************************
 * Template for functional testing instructions with basic data
 ******************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, 0, dstride)
 *****************************************************************************/
/**
 * Template for functional testing with basic data
 *
 * @testnum  test case number
 * @inst     inst to test
 * @result   start addr for test result
 * @val      source floating number
 * @width    matrix width
 * @height   matrix height
 * @stride   stride of result matrix
 */
#define TEST_MOVE_FLOAT_TEMPLATE(testnum, inst, result, val, width, height, stride) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, stride) \
  flw ft0, val; \
  la a0, RD_ADDR; \
  inst (a0), ft0; \
  COPY_STRIDE_S(test_##testnum##_data, RD_ADDR, height, width, stride, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, height*width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection


/*******************************************************************************
 * Template for functional testing instructions to move floating number and
 * expand it to a matrix, the instruction will trigger the specified exception.
 *****************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, 0, stride)
 *****************************************************************************/
/**
 * Template for functional testing with specified exception
 *
 * @testnum      test case number
 * @inst         inst to test
 * @result       start addr for test result
 * @val          source floating number
 * @width        width of result matrix
 * @height       height of result matrix
 * @doff         offset of dest operand
 * @stride       stride of result matrix
 * @dest_addr    address to save dest matrix
 * @exception    the specified exception to be tested
 */
#define TEST_MOVE_FLOAT_WITH_EXCEPTION_TEMPLATE(testnum, inst, result, val, \
                                              width, height, doff, stride, \
                                              dest_addr, exception) \
test_ ## testnum: \
  TEST_EXCEPTION(exception, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(height, width, 0, dstride) \
  flw ft0, val; \
  la a1, dest_addr+doff; \
  inst (a1), ft0; \
  j fail; \
test_ ## testnum ## _end: \

/*******************************************************************************
 * Template for functional testing with basic data
 ******************************************************************************
 * NOTE: To use this template to construct test case, the following macros must
 *       be defined according the instruction to be tested:
 *       1) SETCSR: set the corresponding CSRs using the argument list
 *                   (height, width, sstride, dstride)
 *****************************************************************************/
/**
 * Template for functional testing to move matrix with basic data
 *
 * @testnum      test case number
 * @inst         inst to test
 * @result       start addr for test result
 * @val          start addr for source matrix
 * @width        matrix width
 * @height       matrix height
 * @dstride      stride of result matrix
 * @sstride      stride of source matrix
 * @dest_addr    address to save dest matrix
 * @src_addr     address to save source matrix
 * @mte_coremap  bitfield of enable cores
 */
#define TEST_MOVE_MAT_PERF_TEMPLATE( testnum, inst, result, val, width, height, \
                                dstride, sstride, dest_addr, src_addr, mte_coremap) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  csrr t0, tid;     \
  andi t0, t0, 0x7; \
  li t1, 1;         \
  sll t0, t1, t0;   \
  andi t0, t0, mte_coremap;  \
  bnez t0, 221f;    \
211: \
  PERF_NOP(); \
  j 231f ; \
221: \
  SETCSR(height, width, sstride, dstride) \
  PERF_BEGIN() \
  la a0, src_addr; \
  la a1, dest_addr; \
  inst (a1), (a0); \
  PERF_END8(width ## _ ## height ## _ ## testnum) \
231: \
  fence.i; \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), ESIZE, 0; \
  .popsection

#endif // __TEST_MACROS_MOVE_COMMON_H
