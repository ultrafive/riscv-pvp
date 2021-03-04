#ifndef __TEST_MACRO_VEXXX_MF_H
#define __TEST_MACRO_VEXXX_MF_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#ifndef INST
#error INST must be defined
#endif

#undef RD_ADDR
#undef RS1_ADDR

#if defined(X8_HF_MF)
// vexxx.x8.hf.mf
#define ESIZE_IN    2
#define LDINS_IN    lh
#define STINS_IN    sh
#define ESIZE_OUT   1
#define LDINS_OUT   lb
#define STINS_OUT   sb

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_INT8_CLOSE(vec1, vec2, vlen, 1)

#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc00d5554

#elif defined(X32_MF)
// vexxx.x32.mf
#define ESIZE_IN    4
#define LDINS_IN    lw
#define STINS_IN    sw
#define ESIZE_OUT   2
#define LDINS_OUT   lh
#define STINS_OUT   sh

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.001, 5)

#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc006aaa8

#else
// vexxx.mf
#define ESIZE_IN    2
#define LDINS_IN    lh
#define STINS_IN    sh
#define ESIZE_OUT   2
#define LDINS_OUT   lh
#define STINS_OUT   sh

#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF(vec1, vec2, vlen, 0.001, 5)

#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc0000020

#endif

#define COPY_IN(dst, src, len) COPY(dst, src, len, LDINS_IN, STINS_IN, ESIZE_IN)
#define COPY_OUT(dst, src, len) COPY(dst, src, len, LDINS_OUT, STINS_OUT, ESIZE_OUT)

#define COPY_IN_STRIDE(dst, src, h, w, stride) COPY_STRIDE_D(dst, src, h, w, stride, LDINS_IN, STINS_IN, ESIZE_IN)
#define COPY_OUT_STRIDE(dst, src, h, w, stride) COPY_STRIDE_S(dst, src, h, w, stride, LDINS_OUT, STINS_OUT, ESIZE_OUT)

/* Set RS1 shapes, RS2 is fp16 needn't set shapes,
[31:16]: rs1 width, [15:0] rs1 height*/
#define SET_SHAPES(height, width) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0;

/*Set stride, stride_s[31:16]:rs2 stride, [15:0]:rs1 stride, 
stride_d[15:0]: rd stride*/
#define SET_STRIDES(stride_s1, stride_rd) \
  li a0, stride_s1; \
  li a1, stride_rd; \
  csrw stride_s, a0; \
  csrw stride_d, a1;

/* Functional tests with vexxx_mf shapes
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2 fp
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 */
#define VEXXX_MF(testnum, inst, result, val1, val2, height, width) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(0, 0) \
  \
  la  a2, val2;  \
  flw fa0, (a2); \
  COPY_IN(RS1_ADDR, val1, height * width) \
  \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  inst (a0), (a1), fa0; \
  PERF_END(width ## _ ## height) \
  \
  COPY_OUT(test_ ## testnum ## _data, RD_ADDR, height * width) \
  EQM(result, test_ ## testnum ## _data, height * width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE_OUT, 0; \
  .popsection

/* Functional tests with vexxx_mf stride
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2 fp
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_rd RD matrix stride
 */
#define VEXXX_MF_STRIDE(testnum, inst, result, val1, val2, height, width, stride_s1, stride_rd) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(stride_s1, stride_rd) \
  \
  COPY_IN_STRIDE(RS1_ADDR, val1, height, width, stride_s1) \
  la  a2, val2;  \
  flw fa0, (a2); \
  \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  inst (a0), (a1), fa0; \
  PERF_END(width ## _ ## height ## _ ## stride_s1 ## _ ##testnum) \
  \
  COPY_OUT_STRIDE(test_ ## testnum ## _data, RD_ADDR, height, \
      width, stride_rd) \
  EQM(result, test_ ## testnum ## _data, height * width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE_OUT, 0; \
  .popsection

/* Functional tests with vexxx_mf base addr misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @off_s1    RS1 matrix base addr offset
 * @off_d     RD matrix base addr offset
 */
#define VEXXX_MF_MISALIGNED_BASE_ADDR(testnum, inst, height, width, off_s1, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end) \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(0, 0) \
  \
  la a0, RD_ADDR + off_d; \
  la a1, RS1_ADDR + off_s1; \
  inst (a0), (a1), fa0; \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with vexxx_mf  misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_rd RD matrix stride
 */
#define VEXXX_MF_MISALIGNED_STRIDE(testnum, inst, height, width, stride_s1, stride_rd) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(stride_s1, stride_rd) \
  \
  PERF_BEGIN() \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  inst (a0), (a1), fa0; \
  PERF_END(width ## _ ## height## _ ##testnum) \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with vexxx_mf rs1 and rd address overlapping
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2 fp
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 */
#define VEXXX_MF_RS1_RD_OVERLAPPING(testnum, inst, result, val1, val2, height, width) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(0, 0) \
  \
  la  a2, val2;  \
  flw fa0, (a2); \
  COPY_IN(RS1_ADDR, val1, height * width) \
  \
  la a0, RS1_ADDR; \
  la a1, RS1_ADDR; \
  inst (a0), (a1), fa0; \
  \
  COPY_OUT(test_ ## testnum ## _data, RS1_ADDR, height * width) \
  EQM(result, test_ ## testnum ## _data, height * width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE_OUT, 0; \
  .popsection

/**
 * Invalid params exception
 *
 * @testnum   test case number
 * @inst      inst to test
 * @height    matrix height
 * @width     matrix width
 */
#define VEXXX_MF_INVALID_PARAM(testnum, inst, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(0, 0) \
  \
  la a0, RD_ADDR; \
  la a1, RS1_ADDR; \
  inst (a0), (a1), fa0; \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault exception
 *
 * @testnum   test case number
 * @inst      inst to test
 * @ result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2 fp
 * @height    matrix height
 * @width     matrix width
 */
#define VEXXX_MF_ACCESS_FAULT(testnum, inst, result, val1, val2, height, width) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_SHAPES(height, width) \
  SET_STRIDES(0, 0) \
  \
  la a0, result; \
  la a1, val1; \
  la  a2, val2;  \
  flw fa0, (a2); \
  inst (a0), (a1), fa0; \
  j fail; \
test_ ## testnum ## _end: \

/*
  Public test case wrappers
*/
#define TEST_VEXXX_MF(num, height, width) \
  VEXXX_MF(num, INST, t##num##_rd, t##num##_rs1, t##num##_rs2, height, width)

#define TEST_VEXXX_MF_STRIDE(num, height, width, stride_s1, stride_rd) \
  VEXXX_MF_STRIDE(num, INST, t##num##_rd, t##num##_rs1, t##num##_rs2,\
    height, width, stride_s1, stride_rd)

#define TEST_VEXXX_MF_ADDR_OVERLAPPING(num, height, width) \
  VEXXX_MF_RS1_RD_OVERLAPPING(num, INST, t##num##_rd, t##num##_rs1, t##num##_rs2, height, width)

#define TEST_VEXXX_MF_MISALIGNED_BASE_ADDR(num, height, width, off_s1, off_d) \
  VEXXX_MF_MISALIGNED_BASE_ADDR(num, INST, height, width, off_s1, off_d)

#define TEST_VEXXX_MF_MISALIGNED_STRIDE(num, height, width, stride_s1, stride_rd) \
  VEXXX_MF_MISALIGNED_STRIDE(num, INST, height, width, stride_s1, stride_rd)

#define TEST_VEXXX_MF_INVALID_PARAM(testnum, height, width) \
  VEXXX_MF_INVALID_PARAM(testnum, INST, height, width)

#define TEST_VEXXX_MF_ACCESS_FAULT(testnum, result, val1, val2, height, width) \
  VEXXX_MF_ACCESS_FAULT(testnum, INST, result, val1, val2, height, width)

#endif
