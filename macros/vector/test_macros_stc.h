// See LICENSE for license details.

#ifndef __TEST_MACROS_STC_H
#define __TEST_MACROS_STC_H

#include "check_eq.h"

#define RD_ADDR   0xc0000000
#define RS1_ADDR  0xc0080000
#define RS2_ADDR  0xc0100000

#define LLB_ADDR  0xF8000000
#define IMB_ADDR  0xC0400000
#define IMB_END   0xC0440000
#define L1B_ADDR  0xC0000000
#define L1B_END   0xC0140000

#ifdef __clang__
  #define dim_h	0
  #define dim_w	1
  #define ts 1
#endif

#define VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, ebyte, ldins) \
    li a4, vlen;    \
    la a5, vec1;    \
    la a6, vec2;    \
  1:                \
    ldins t0, 0(a5);   \
    ldins t1, 0(a6);   \
    li t4, MASK_XLEN(0xfffffffffffffff0); \
    and t2, t0, t4; \
    and t3, t1, t4; \
    /* t3 = abs(t2, t3) */ \
    sub t2, t2, t3; \
    srai t3, t2,0x1f; \
    xor t2, t2, t3; \
    sub t3, t2, t3; \
    li t2, 0xfffc0; \
    and t3, t3, t2; \
    li t4, 0; \
    beq t4, t3, 2f;   \
    j fail; \
   2: \
    addi a5, a5, ebyte;  \
    addi a6, a6, ebyte;  \
    addi a4, a4, -1;    \
    bnez a4, 1b;        \

// check if equal on two vectors with float elements
#define VV_HF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, 2, lh)
#define VV_SF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, 4, lw)
#define VV_DF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, 8, ld)

#-----------------------------------------------------------------------
# RV STC Custom MACROS
#-----------------------------------------------------------------------

#define COPY(to, from, len, ldins, stins, esize) \
  la t0, from; \
  la t1, to; \
  li t2, len; \
1: \
  ldins t3, 0(t0); \
  stins t3, 0(t1); \
  addi t0, t0, esize; \
  addi t1, t1, esize; \
  addi t2, t2, -1; \
  bnez t2, 1b;

/* Strided copy - the `from` data is strided */
#define COPY_STRIDE_S(to, from, height, width, stride, ldins, stins, esize) \
  la t4, from; \
  la t1, to; \
  li t2, height; \
1: \
  li t3, width; \
  mv t0, t4; \
2: \
  ldins t5, 0(t0); \
  stins t5, 0(t1); \
  addi t0, t0, esize; \
  addi t1, t1, esize; \
  addi t3, t3, -1; \
  bnez t3, 2b; \
  li t5, stride; \
  bnez t5, 3f; \
  li t5, width * esize; \
3: \
  add t4, t4, t5; \
  addi t2, t2, -1; \
  bnez t2, 1b;

/* Strided copy - the `to` data is strided */
#define COPY_STRIDE_D(to, from, height, width, stride, ldins, stins, esize) \
  la t4, to; \
  la t0, from; \
  li t2, height; \
1: \
  li t3, width; \
  mv t1, t4; \
2: \
  ldins t5, 0(t0); \
  stins t5, 0(t1); \
  addi t0, t0, esize; \
  addi t1, t1, esize; \
  addi t3, t3, -1; \
  bnez t3, 2b; \
  li t5, stride; \
  bnez t5, 3f; \
  li t5, width * esize; \
3: \
  add t4, t4, t5; \
  addi t2, t2, -1; \
  bnez t2, 1b;

#-----------------------------------------------------------------------
# Tests for .mm instructions
#-----------------------------------------------------------------------
#define TEST_STC_MM_OP2_INTERNAL( testnum, inst, result, val1, val2, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  li a1, (width << 16 + height); \
  csrw shape_s1, a0; \
  csrw shape_s2, a1; \
  li a0, (width * height); \
  la a1, val1; \
  la a2, val2; \
  la a3, RS1_ADDR; \
  la a4, RS2_ADDR; \
1: \
  ldins a5, 0(a1); \
  ldins a6, 0(a2); \
  stins a5, 0(a3); \
  stins a6, 0(a4); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a4, a4, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  la a4, RS2_ADDR; \
  inst (a2), (a3), (a4); \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MM_HF_OP2( testnum, inst, result, val1, val2, width, height ) \
  TEST_STC_MM_OP2_INTERNAL(testnum, inst, result, val1, val2, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for .mf instructions
#-----------------------------------------------------------------------
#define TEST_STC_MF_OP2_INTERNAL( testnum, inst, result, val1, val2, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  li a1, (width << 16 + height); \
  csrw shape_s1, a0; \
  li a0, (width * height); \
  la a1, val1; \
  la a2, val2; \
  flw fa0, (a2); \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3), fa0; \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MF_HF_OP2( testnum, inst, result, val1, val2, width, height ) \
  TEST_STC_MF_OP2_INTERNAL(testnum, inst, result, val1, val2, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for .mv instructions
#-----------------------------------------------------------------------
#define TEST_STC_MV_OP2_INTERNAL( testnum, inst, result, val1, val2, width, height, vlen, dim, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a2, RS1_ADDR; \
1: \
  ldins a3, 0(a1); \
  stins a3, 0(a2); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  li a0, vlen; \
  la a1, val2; \
  la a2, RS2_ADDR; \
2: \
  ldins a3, 0(a1); \
  stins a3, 0(a2); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  la a4, RS2_ADDR; \
  inst (a2), (a3), (a4), dim; \
  \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
3: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 3b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MV_HF_OP2( testnum, inst, result, val1, val2, width, height, vlen, dim ) \
  TEST_STC_MV_OP2_INTERNAL(testnum, inst, result, val1, val2, width, height, vlen, dim, 16, lh, sh, VV_HF_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .m instructions
#-----------------------------------------------------------------------
#define TEST_STC_M_OP1_INTERNAL( testnum, inst, result, val1, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3); \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_M_HF_OP1( testnum, inst, result, val1, width, height ) \
  TEST_STC_M_OP1_INTERNAL(testnum, inst, result, val1, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for .m acc all instructions
#-----------------------------------------------------------------------
#define TEST_STC_M_ACC_ALL_OP1_INTERNAL( testnum, inst, result, val1, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  la a3, RS1_ADDR; \
  inst fa2, (a3); \
  la a0, result; \
  flw fa1, 0(a0); \
  feq.s a0, fa1, fa2; \
  li a1, 1; \
  beq a0, a1, 2f; \
  j fail;
2:;

#define TEST_STC_M_ACC_ALL_HF_OP1( testnum, inst, result, val1, width, height ) \
  TEST_STC_M_ACC_ALL_OP1_INTERNAL(testnum, inst, result, val1, width, height, 16, lh, sh, VV_HF_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .m acc dim0/dim_h instructions
#-----------------------------------------------------------------------
#define TEST_STC_M_ACC_DM0_OP1_INTERNAL( testnum, inst, result, val1, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3), dim_h; \
  li a0, (width * 1); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * 1)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_M_ACC_DM0_HF_OP1( testnum, inst, result, val1, width, height ) \
  TEST_STC_M_ACC_DM0_OP1_INTERNAL(testnum, inst, result, val1, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for .m acc dim1 instructions
#-----------------------------------------------------------------------
#define TEST_STC_M_ACC_DM1_OP1_INTERNAL( testnum, inst, result, val1, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3), dim_w; \
  li a0, (1 * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (1 * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_M_ACC_DM1_HF_OP1( testnum, inst, result, val1, width, height ) \
  TEST_STC_M_ACC_DM1_OP1_INTERNAL(testnum, inst, result, val1, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for mov.v instructions
#-----------------------------------------------------------------------
#define TEST_STC_MOV_V_OP1_INTERNAL( testnum, inst, result, val1, width, height, dim, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3), dim; \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MOV_V_HF_OP1( testnum, inst, result, val1, width, height, dim ) \
  TEST_STC_MOV_V_OP1_INTERNAL(testnum, inst, result, val1, width, height, dim, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for mov.f instructions
#-----------------------------------------------------------------------
#define TEST_STC_MOV_F_OP1_INTERNAL( testnum, inst, result, val1, width, height, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw shape_s1, a0; \
  \
  la a1, val1; \
  flw fa0, (a1); \
  \
  la a2, RD_ADDR; \
  inst (a2), fa0; \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MOV_F_HF_OP1( testnum, inst, result, val1, width, height ) \
  TEST_STC_MOV_F_OP1_INTERNAL(testnum, inst, result, val1, width, height, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for pld/mov.l1.llb instructions
#-----------------------------------------------------------------------
#define TEST_STC_MOV_IN_OP1_INTERNAL( testnum, inst, result, val1, width, height, coremap, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw mte_shape, a0; \
  li a0, (width * ebits/8); \
  csrw mte_stride_llb, a0; \
  li a0, coremap; \
  csrw mte_coremap, a0; \
  li a0, (width * height); \
  la a1, val1; \
  la a3, LLB_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  la a2, RD_ADDR; \
  la a3, LLB_ADDR; \
  inst (a2), (a3); \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MOV_IN_HF_OP1( testnum, inst, result, val1, width, height, coremap ) \
  TEST_STC_MOV_IN_OP1_INTERNAL(testnum, inst, result, val1, width, height, coremap, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for mov.llb.l1 instructions
#-----------------------------------------------------------------------
#define TEST_STC_MOV_OUT_OP1_INTERNAL( testnum, inst, result, val1, width, height, coremap, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  csrw mte_shape, a0; \
  li a0, (width * ebits/8); \
  csrw mte_stride_llb, a0; \
  li a0, coremap; \
  csrw mte_coremap, a0; \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  la a2, LLB_ADDR; \
  la a3, RS1_ADDR; \
  inst (a2), (a3); \
  li a0, (width * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MOV_OUT_HF_OP1( testnum, inst, result, val1, width, height, coremap ) \
  TEST_STC_MOV_OUT_OP1_INTERNAL(testnum, inst, result, val1, width, height, coremap, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for memul.mm instructions
#-----------------------------------------------------------------------
#define TEST_STC_MATMUL_OP2_INTERNAL( testnum, inst, result, val1, val2, height, width, width2, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (width << 16 + height); \
  li a1, (width2 << 16 + width); \
  csrw m_shape_s1, a0; \
  csrw m_shape_s2, a1; \
  \
  li a0, (width * height); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  li a0, (width2 * width); \
  la a1, val2; \
  la a3, RS2_ADDR; \
2: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  la a4, RS2_ADDR; \
  inst (a2), (a3), (a4); \
  li a0, (width2 * height); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (width2 * height)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (width2 * height), (ebits/8), 0; \
  .popsection

#define TEST_STC_MATMUL_HF_OP2( testnum, inst, result, val1, val2, height, width, width2 ) \
  TEST_STC_MATMUL_OP2_INTERNAL(testnum, inst, result, val1, val2, height, width, width2, 16, lh, sh, VV_HF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for meconv.mm instructions
#-----------------------------------------------------------------------
#define TEST_STC_MECONV_OP2_INTERNAL( testnum, inst, result, val1, val2, inh, inw, inc, inc_stride, kh, kw, outc, outc_stride, outh, outw, padu,padd,padl,padr, sliding, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  li a0, (inw << 16 + inh); \
  csrw conv_FM_in, a0; \
  li a0, (kw << 24 + kh << 16 + 1 << 8 + sliding); \
  csrw conv_kernel, a0; \
  li a0, (outw << 16 + outh); \
  csrw conv_FM_out, a0; \
  li a0, (inc_stride << 16 + inc); \
  csrw conv_Depth_in, a0; \
  li a0, (outc_stride << 16 + outc); \
  csrw conv_Depth_out, a0; \
  li a0, (padu << 24 + padd << 16 + padl << 8 + padr); \
  csrw conv_padding, a0; \
  \
  li a0, (inh * inw * inc); \
  la a1, val1; \
  la a3, RS1_ADDR; \
1: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 1b; \
  \
  li a0, (kh * kw * inc * outc); \
  la a1, val2; \
  la a3, RS2_ADDR; \
2: \
  ldins a5, 0(a1); \
  stins a5, 0(a3); \
  addi a1, a1, (ebits/8); \
  addi a3, a3, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  \
  la a2, RD_ADDR; \
  la a3, RS1_ADDR; \
  la a4, RS2_ADDR; \
  inst (a2), (a3), (a4); \
  li a0, (outh * outw * outc); \
  la a1, test_ ## testnum ## _data; \
2: \
  ldins a3, 0(a2); \
  stins a3, 0(a1); \
  addi a1, a1, (ebits/8); \
  addi a2, a2, (ebits/8); \
  addi a0, a0, -1; \
  bnez a0, 2b; \
  eqm(result, test_ ## testnum ## _data, (outh * outw * outc)); \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill (outh * outw * outc), (ebits/8), 0; \
  .popsection

#define TEST_STC_MECONV_HF_OP2( testnum, inst, result, val1, val2, inh, inw, inc, inc_stride, kh, kw, outc, outc_stride, outh, outw, padu,padd,padl,padr, sliding) \
  TEST_STC_MECONV_OP2_INTERNAL(testnum, inst, result, val1, val2, inh, inw, inc, inc_stride, kh, kw, outc, outc_stride, outh, outw, padu,padd,padl,padr, sliding, 16, lh, sh, VV_HF_CHECK_EQ)


#endif
