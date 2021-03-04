#ifndef __TEST_MACRO_VEEMACC_H
#define __TEST_MACRO_VEEMACC_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

//L1 buffer start 0xc0000000, buffer size 0x140000
#define VEADD_RD_ADDR   0xc0000000
#define VEADD_RS1_ADDR  0xc006aaaa //0xc006aaa8
#define VEADD_RS2_ADDR  0xc00d5554
#define ESIZE 2
#define LDINS lh
#define STINS sh
#define EQM(vec1, vec2, vlen) VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, 0.05, 1, vlen+1)

/* Set RS1 shapes, RS2 is fp16 needn't set shapes,
[31:16]: rs1 width, [15:0] rs1 height*/
#define SET_VEEMACC_SHAPES(height, width) \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0;

/*Set stride_s, stride_s[31:16]:rs2 stride, [15:0]:rs1 stride*/
#define SET_VEEMACC_STRIDE(stride_s1, stride_s2, stride_rd) \
  li a0,  (stride_s2 <<  16 + stride_s1); \
  li a1,  stride_rd; \
  csrw stride_s, a0; \
  csrw stride_d, a1;

  #define MEEMACC_ALL_SUM_CHECK(fp0, fp1, abs_epsilon, acc) \
    la t0, 51f; \
    flw ft0, 0(t0); \
    /* abs_epsilon = (abs_epsilon * acc) */ \
    li t0, acc; \
    fcvt.s.w ft1, t0; \
    fmul.s ft3, ft1, ft0; \
    \
    feq.s t0, fp0, fp1; \
    bnez t0, 50f; \
    \
     /* Calculate absolute diffence and compare with fa0 */ \
    fsub.s fp0, fp0, fp1; \
	  fabs.s fp0, fp0; \
	  flt.s t0, fp0, ft3; \
	  bnez t0, 50f; \
    j fail; \
  \
  50: \
    .pushsection .data; \
    .align 4; \
  51: \
    .float abs_epsilon; \
    .float 2.0; \
    .popsection

    
/* Functional tests  veemacc.mm/mv  shapes and stride with all sum
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr RS1 matrix1
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_s2 RS2 matrix stride
 */
#define VEEMACC_ALL_SUM(testnum, inst, result, val1, val2, height, width, stride_s1, stride_s2) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, stride_s2, 0) \
  \
  COPY_STRIDE_D(VEADD_RS1_ADDR, val1, height, width, stride_s1, LDINS, STINS, ESIZE) \
  COPY_STRIDE_D(VEADD_RS2_ADDR, val2, height, width, stride_s2, LDINS, STINS, ESIZE) \
  \
  PERF_BEGIN() \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst fa0, (a1), (a2); \
  PERF_END(width ## _ ## height ## _ ## stride_s1 ## _ ## stride_s2 ## _ ## testnum) \
  la a3, result; \
  flw fa1, (a3); \
  \
  MEEMACC_ALL_SUM_CHECK(fa0, fa1, 0.005, height * width); \
  \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/* Functional tests  veemacc.mm/mv shapes and stride with dim_h
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr RS1 matrix1
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @height2   RS2 matrix height
 * @width2    RS2 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_s2 RS2 matrix stride
 * @stride_rd RD matrix stride
 */
#define VEEMACC_DIM_H(testnum, inst, result, val1, val2, height, width, height2, width2, stride_s1, stride_s2, stride_rd) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, stride_s2, stride_rd) \
  \
  COPY_STRIDE_D(VEADD_RS1_ADDR, val1, height, width, stride_s1, LDINS, STINS, ESIZE) \
  COPY_STRIDE_D(VEADD_RS2_ADDR, val2, height2, width2, stride_s2, LDINS, STINS, ESIZE) \
  \
  PERF_BEGIN() \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst (a0), (a1), (a2), dim_h; \
  PERF_END(width ## _ ## height ## _ ## stride_s1 ## _ ## stride_s2 ## _ ## testnum) \
  \
  COPY_STRIDE_S(test_ ## testnum ## _data, VEADD_RD_ADDR, 1, \
    width, stride_rd, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/* Functional tests  veemacc.mm/mv shapes and stride with dim_w
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr RS1 matrix1
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @height2   RS2 matrix height
 * @width2    RS2 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_s2 RS2 matrix stride
 * @stride_rd RD matrix stride
 */
#define VEEMACC_DIM_W(testnum, inst, result, val1, val2, height, width, height2, width2, stride_s1, stride_s2, stride_rd) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, stride_s2, stride_rd) \
  \
  COPY_STRIDE_D(VEADD_RS1_ADDR, val1, height, width, stride_s1, LDINS, STINS, ESIZE) \
  COPY_STRIDE_D(VEADD_RS2_ADDR, val2, height2, width2, stride_s2, LDINS, STINS, ESIZE) \
  \
  PERF_BEGIN() \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst (a0), (a1), (a2), dim_w; \
  PERF_END(width ## _ ## height ## _ ## stride_s1 ## _ ## stride_s2 ## _ ## testnum) \
  \
  COPY_STRIDE_S(test_ ## testnum ## _data, VEADD_RD_ADDR, height, \
    1, stride_rd, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, height); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/* Functional tests  veemacc.mf shapes and stride with dim_h
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr RS1 matrix1
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 */
#define VEEMACC_DIM_H_MF(testnum, inst, result, val1, val2, height, width, stride_s1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, 0, 0) \
  \
  COPY_STRIDE_D(VEADD_RS1_ADDR, val1, height, width, stride_s1, LDINS, STINS, ESIZE) \
  \
  la  a2, val2;  \
  flw fa0, (a2); \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  \
  inst (a0), (a1), fa0, dim_h; \
  \
  COPY(test_ ## testnum ## _data, VEADD_RD_ADDR, width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/* Functional tests  veemacc.mf shapes and stride with dim_w
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr RS1 matrix1
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 */
#define VEEMACC_DIM_W_MF(testnum, inst, result, val1, val2, height, width, stride_s1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, 0, 0) \
  \
  COPY_STRIDE_D(VEADD_RS1_ADDR, val1, height, width, stride_s1, LDINS, STINS, ESIZE) \
  \
  la  a2, val2;  \
  flw fa0, (a2); \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  inst (a0), (a1), fa0, dim_w; \
  \
  COPY(test_ ## testnum ## _data, VEADD_RD_ADDR, height, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, height); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/* Functional tests with veemacc.mm/mv base addr misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @dim       dim
 * @off_s1    RS1 matrix base addr offset
 * @off_s2    RS2 matrix base addr offset
 * @off_d     RD matrix base addr offset
 */
#define VEEMACC_MISALIGNED_BASE_ADDR(testnum, inst, dim, height, width, off_s1, off_s2, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end) \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a0, VEADD_RD_ADDR + off_d; \
  la a1, VEADD_RS1_ADDR + off_s1; \
  la a2, VEADD_RS2_ADDR + off_s2; \
  inst (a0), (a1), (a2), dim; \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with veemacc.mf base addr misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @dim       dim
 * @off_s1    RS1 matrix base addr offset
 * @off_s2    RS2 matrix base addr offset
 * @off_d     RD matrix base addr offset
 */
#define TEST_VEEMACC_MF_MISALIGNED_BASE_ADDR(testnum, inst, dim, height, width, off_s1, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end) \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la  a2, VEADD_RS2_ADDR;  \
  flw fa0, (a2); \
  la a0, VEADD_RD_ADDR + off_d; \
  la a1, VEADD_RS1_ADDR + off_s1; \
  inst (a0), (a1), fa0, dim; \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests veemacc.mm base addr misaligned with all sum 
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @off_s1    RS1 matrix base addr offset
 * @off_s2    RS2 matrix base addr offset
 */
#define VEEMACC_ALL_MISALIGNED_BASE_ADDR(testnum, inst, height, width, off_s1, off_s2) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end) \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a1, VEADD_RS1_ADDR + off_s1; \
  la a2, VEADD_RS2_ADDR + off_s2; \
  inst fa0, (a1), (a2); \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with veemacc.mm/mv  misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @dim       dim
 * @stride_s1 RS1 matrix stride
 * @stride_s2 RS2 matrix stride
 * @stride_rd RD matrix stride
 */
#define VEEMACC_MISALIGNED_STRIDE(testnum, inst, dim, height, width, stride_s1, stride_s2, stride_rd) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, stride_s2, stride_rd) \
  \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst (a0), (a1), (a2), dim; \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with veemacc.mf  misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @dim       dim
 * @stride_s1 RS1 matrix stride
 */
#define TEST_VEEMACC_MF_MISALIGNED_STRIDE(testnum, inst, dim, height, width, stride_s1) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, 0, 0) \
  \
  \
  la  a2, VEADD_RD_ADDR;  \
  flw fa0, (a2); \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  \
  inst (a0), (a1), fa0, dim; \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with veemacc.mm all misaligned
 * @testnum   test case number
 * @inst      inst to test
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 * @stride_s1 RS1 matrix stride
 * @stride_s2 RS2 matrix stride
 */
#define VEEMACC_ALL_MISALIGNED_STRIDE(testnum, inst, height, width, stride_s1, stride_s2) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(stride_s1, stride_s2, 0) \
  \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst fa0, (a1), (a2); \
  \
  j fail; \
test_ ## testnum ## _end: \

/* Functional tests with veemacc.mm/mv rs1 and rd address overlapping
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 */
#define VEEMACC_DIM_H_RS_RD_OVERLAPPING(testnum, inst, result, val1, val2, height, width, overlap_addr) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  COPY(VEADD_RS1_ADDR, val1, height * width, LDINS, STINS, ESIZE) \
  COPY(VEADD_RS2_ADDR, val2, height * width, LDINS, STINS, ESIZE) \
  \
  la a0, overlap_addr; \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst (a0), (a1), (a2), dim_h; \
  \
  COPY(test_ ## testnum ## _data, overlap_addr,  width, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, width); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection


/* Functional tests with veemacc.mm/mf rs2 and rd address overlapping
 * @testnum   test case number
 * @inst      inst to test
 * @result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2
 * @height    RS1 matrix height
 * @width     RS1 matrix width
 */
#define VEEMACC_DIM_W_RS_RD_OVERLAPPING(testnum, inst, result, val1, val2, height, width, overlap_addr) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  COPY(VEADD_RS1_ADDR, val1, height * width, LDINS, STINS, ESIZE) \
  COPY(VEADD_RS2_ADDR, val2, height * width, LDINS, STINS, ESIZE) \
  \
  la a0, overlap_addr; \
  la a1, VEADD_RS1_ADDR; \
  la a2, VEADD_RS2_ADDR; \
  inst (a0), (a1), (a2), dim_w; \
  \
  COPY(test_ ## testnum ## _data, overlap_addr,  height, LDINS, STINS, ESIZE) \
  EQM(result, test_ ## testnum ## _data, height); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill height * width, ESIZE, 0; \
  .popsection

/**
 * Invalid params exception with veemacc.mm/mv
 *
 * @testnum   test case number
 * @inst      inst to test
 * @dim       dim
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_INVALID_PARAM(testnum, inst, dim, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  la  a2, VEADD_RS2_ADDR;  \
  inst (a0), (a1), (a2), dim; \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Invalid params exception with veemacc.mf
 *
 * @testnum   test case number
 * @inst      inst to test
 * @dim       dim
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_MF_INVALID_PARAM(testnum, inst, dim, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la  a2, VEADD_RD_ADDR;  \
  flw fa0, (a2); \
  la a0, VEADD_RD_ADDR; \
  la a1, VEADD_RS1_ADDR; \
  inst (a0), (a1), fa0, dim; \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Invalid params exception with veemacc.mm all sum
 *
 * @testnum   test case number
 * @inst      inst to test
 * @dim       dim
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_ALL_INVALID_PARAM(testnum, inst, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a1, VEADD_RS1_ADDR; \
  la  a2, VEADD_RS2_ADDR;  \
  inst fa0, (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault exception with veemacc.mm/mv
 *
 * @testnum   test case number
 * @inst      inst to test
 * @ result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2
 * @dim       dim
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_ACCESS_FAULT(testnum, inst, result, val1, val2, dim, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a0, result; \
  la a1, val1; \
  la  a2, val2;  \
  inst (a0), (a1), (a2), dim; \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault exception with veemacc.mf
 *
 * @testnum   test case number
 * @inst      inst to test
 * @ result    start addr for test result
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2
 * @dim       dim
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_MF_ACCESS_FAULT(testnum, inst, result, val1, val2, dim, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la  a2, VEADD_RD_ADDR;  \
  flw fa0, (a2); \
  la a0, result; \
  la a1, val1; \
  inst (a0), (a1), fa0, dim; \
  j fail; \
test_ ## testnum ## _end: \

/**
 * Access fault exception with veemacc.mm all sum
 *
 * @testnum   test case number
 * @inst      inst to test
 * @val1      start addr RS1 matrix1
 * @val2      start addr for RS2
 * @height    matrix height
 * @width     matrix width
 */
#define TEST_VEEMACC_ALL_ACCESS_FAULT(testnum, inst, val1, val2, height, width) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  \
  SET_VEEMACC_SHAPES(height, width) \
  SET_VEEMACC_STRIDE(0, 0, 0) \
  \
  la a1, val1; \
  la  a2, val2;  \
  inst fa0, (a1), (a2); \
  j fail; \
test_ ## testnum ## _end: \


#endif
