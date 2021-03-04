#ifndef __VEXX_XX_M_H
#define __VEXX_XX_M_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"


#if defined(VEXX_HF_X8_M)
#define SLDINS lb
#define SSTINS sb
#define SESIZE 1

#define DLDINS lh
#define DSTINS sh
#define DESIZE 2
#define EQM(vec1, vec2, vlen)  VV_CHECK_EQ_INT8(vec1, vec2, vlen)

#elif defined(VEXX_X8_HF_M)
#define SLDINS lh
#define SSTINS sh
#define SESIZE 2

#define DLDINS lb
#define DSTINS sb
#define DESIZE 1
#define EQM(vec1, vec2, vlen)  VV_CHECK_EQ_INT8(vec1, vec2, vlen)
#elif defined (VEXX_M_DEFAULT)
#define SLDINS lh
#define SSTINS sh
#define SESIZE 2

#define DLDINS lh
#define DSTINS sh
#define DESIZE 2
#define EQM(vec1, vec2, vlen)   VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, 0.005, VV_CHECK_EQ_HF_RTOL, vlen)
#endif

#define COPY_IN_STRIDE(dst, src, h, w, stride) COPY_STRIDE_D(dst, src, h, w, stride, SLDINS, SSTINS, SESIZE)
#define COPY_OUT_STRIDE(dst, src, h, w, stride) COPY_STRIDE_S(dst, src, h, w, stride, DLDINS, DSTINS, DESIZE)

//split l1buffer into 2 blocks of same size
#define VECAT_RD_ADDR  0xC0000000
#define VECAT_RS_ADDR  0xc00A0000

#define SET_SHAPES(height, width) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0;

#define SET_STRIDE(stride_dst, stride_s1) \
  li a0, stride_s1; \
  csrw stride_s, a0; \
  li a1, stride_dst; \
  csrw stride_d, a1;

/*Functional tests with basic data
 *
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix
 * @height    matrix height
 * @width     matrix width
 * @stride_s1  RS1 matrix stride
 * @stride_dst RD matrix stride
 */
#define VECVT_M_INTERNAL(testnum, inst, result, val1, height, width, stride_dst, stride_s1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDE(stride_dst, stride_s1) \
  \
  COPY_IN_STRIDE(VECAT_RS_ADDR, val1, height, width, stride_s1) \
  PERF_BEGIN() \
  la a0, VECAT_RD_ADDR; \
  la a1, VECAT_RS_ADDR; \
  inst (a0), (a1); \
  PERF_END(width ## _ ## height ## _ ## stride_s1 ## _ ## testnum) \
  COPY_OUT_STRIDE(test_ ## testnum ## _data, VECAT_RD_ADDR, height, width, stride_dst) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), DESIZE, 0; \
  .popsection

/*Functional tests with inplace compute on rs1
 * rd = rs1
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr for source matrix
 * @width     matrix width
 * @height    matrix height
 */
#define VEXX_XX_M_INPLACE_RS1_INTERNAL(testnum, inst, result, val1, height, width) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  COPY(VECAT_RS_ADDR, val1, height*width, SLDINS, SSTINS, SESIZE) \
  SET_SHAPES(height, width) \
  SET_STRIDE(0, 0) \
  la a1, VECAT_RS_ADDR; \
  inst (a1), (a1); \
  COPY(test_ ## testnum ## _data, VECAT_RS_ADDR, height*width, DLDINS, DSTINS, DESIZE) \
  EQM(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), DESIZE, 0; \
  .popsection

/**
 * Misaligned base address for operands
 *
 * @testnum   test case number
 * @inst      inst to test
 * @width     matrix width
 * @height    matrix height
 * @doff      address offset for dest operand
 * @soff1     address offset for source operand 1
 */
#define TEST_VEXX_XX_M_MISALIGNED_BASE(testnum, inst, height, width, doff, soff1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SET_SHAPES(height, width) \
  SET_STRIDE(0, 0) \
  PERF_BEGIN() \
  li a0, VECAT_RD_ADDR + doff; \
  li a1, VECAT_RS_ADDR + soff1; \
  inst (a0), (a1); \
  PERF_END(width ## _ ## height ## _ ## testnum) \
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
#define TEST_VEXX_XX_M_INVALID_PARAM(testnum, inst, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SET_SHAPES(height, width) \
  SET_STRIDE(0, 0) \
  li a0, VECAT_RD_ADDR; \
  li a1, VECAT_RS_ADDR; \
  inst (a0), (a1); \
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
 */
#define TEST_VEXX_XX_M_MISALIGNED_STRIDE(testnum, inst, height, width, dstride, sstride1) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SET_SHAPES(height, width) \
  SET_STRIDE(dstride, sstride1) \
  PERF_BEGIN() \
  li a0, VECAT_RD_ADDR; \
  li a1, VECAT_RS_ADDR; \
  inst (a0), (a1); \
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
 */
#define TEST_VEXX_XX_M_ACCESS_FAULT(testnum, inst, dst, src1, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SET_SHAPES(height, width) \
  SET_STRIDE(0, 0) \
  li a0, dst; \
  li a1, src1; \
  inst (a0), (a1); \
  j fail; \
test_ ## testnum ## _end: \

#endif
