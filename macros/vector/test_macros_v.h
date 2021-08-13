// See LICENSE for license details.

#ifndef __TEST_MACROS_VECTOR_H
#define __TEST_MACROS_VECTOR_H

#include "check_eq.h"

#-----------------------------------------------------------------------
# RV VECTOR MACROS
#-----------------------------------------------------------------------
#define VLMAX (8*VLEN/8)

#define VSHIFT8  0
#define VSHIFT16 1
#define VSHIFT32 2
#define VSHIFT64 3

#define VREG_0    v0
#define VREG_1    v1
#define VREG_2    v2
#define VREG_3    v3
#define VREG_4    v4

#define VM_0 ,v0.t
#define VM_1
#define VM_2 ,v0

#define ZERO_ZONE 0xc0000000
#define RD_ADDR   0xc0000100
#define RS1_ADDR  0xc0040000
#define RS2_ADDR  0xc0080000
#define MASK_ADDR  0xc0100000
#define RD_PRELOAD_ADDR  0xc0110000

#define LLB_ADDR  0xF8000000
#define IMB_ADDR  0xC0400000
#define L1B_ADDR  0xC0000000

#-----------------------------------------------------------------------
# RV STC Custom MACROS
#-----------------------------------------------------------------------
#define SET_ZERO(addr, len) \
  li t1 ,0 ; \
  la t2, addr ; \
  la t3, len ; \
3: \
  sw t1, (t2) ; \
  addi t3, t3, -4 ; \
  addi t2, t2, 4 ; \
  bnez t3, 3b ;

#define SET_ZERO_MUL_T3(addr, len) \
  li t1 ,0 ; \
  la t2, addr ; \
  la t4, len ; \
  mul t3, t3, t4 ; \
3: \
  sw t1, (t2) ; \
  addi t3, t3, -4 ; \
  addi t2, t2, 4 ; \
  bnez t3, 3b ;

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

#define COPY_STRIDE_SRC(start, end, from, len, nf, stride, eew) \
  li a0, start; \
  li a1, end; \
  li a3, len; \
  li a2, (start+(len-1)*stride+eew); \
  bgt a2, a1, 22f; \
  li a1, stride; \
13: \
  la a2, from; \
11: \
  li a5, eew*nf; \
  mv a6, a0; \
12: \
  lb a4, 0(a2); \
  sb a4, 0(a6); \
  addi a2, a2, 1; \
  addi a6, a6, 1; \
  addi a5, a5, -1; \
  bnez a5, 12b; \
  add a0, a0, a1; \
  addi a3, a3, -1; \
  bnez a3, 11b; \
  j 33f; \
22: \
  j fail; \
33:

#define COPY_STRIDE_DST(from, to, len, nf, stride, eew) \
  li a0, from; \
  la a1, to; \
  li a2, len; \
  li a3, stride; \
  \
11: \
  li a4, eew*nf; \
  mv a6, a0; \
12: \
  lb a5, 0(a6); \
  sb a5, 0(a1); \
  addi a6, a6, 1; \
  addi a1, a1, 1; \
  addi a4, a4, -1;\
  bnez a4, 12b; \
  add a0, a0, a3; \
  addi a2, a2, -1; \
  bnez a2, 11b; \
  j 33f; \
22: \
  j fail; \
33:

#define COPY_INDEX_SRC(start, end, from, len, index, sew, eew, ldins_i, nf) \
  li a0, start; \
  li a1, end; \
  la a2, from; \
  li a3, len; \
  la a4, index; \
  \
11: \
  ldins_i t0, 0(a4); \
  add t1, t0, a0; \
  addi t2, t1, sew*nf; \
  bgt t2, a1, 22f; \
  li t3, sew*nf; \
12: \
  lb a6, 0(a2); \
  sb a6, 0(t1); \
  addi a2, a2, 1; \
  addi t1, t1, 1; \
  addi t3, t3, -1; \
  bnez t3, 12b; \
  addi a4, a4, eew; \
  addi a3, a3, -1; \
  bnez a3, 11b; \
  j 33f; \
22: \
  j fail; \
33:

#define COPY_INDEX_DST(from, to, len, index, sew, eew, start, ldins_i, nf) \
  li t0, from; \
  la t1, to; \
  li a0, sew*nf*start; \
  add t1, t1, a0; \
  li t2, len-start; \
  la t3, index; \
  li a0, eew*start; \
  add t3, t3, a0; \
  \
11: \
  ldins_i t4, 0(t3); \
  add t5, t0, t4; \
  li a1, sew*nf; \
12: \
  lb t6, 0(t5); \
  sb t6, 0(t1); \
  addi t5, t5, 1; \
  addi t1, t1, 1; \
  addi a1, a1, -1; \
  bnez a1, 12b; \
  addi t3, t3, eew; \
  addi t2, t2, -1; \
  bnez t2, 11b; \
  j 33f; \
22: \
  j fail; \
33:

#define VV_CHECK_EQ_INTERNAL(vec1, vec2, vlen, ebyte, ldins) \
    li a4, vlen;    \
    la a5, vec1;    \
    la a6, vec2;    \
  1:                \
    ldins t0, 0(a5);   \
    ldins t1, 0(a6);   \
    beq t0, t1, 2f;   \
    j fail;         \
  2:                \
    addi a5, a5, ebyte;  \
    addi a6, a6, ebyte;  \
    addi a4, a4, -1;    \
    bnez a4, 1b;        \

// check if equal on two vectors with integer elements
#define VV_SB_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_INTERNAL(vec1, vec2, vlen, 1, lb)
#define VV_SH_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_INTERNAL(vec1, vec2, vlen, 2, lh)
#define VV_SW_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_INTERNAL(vec1, vec2, vlen, 4, lw)
#define VV_SD_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_INTERNAL(vec1, vec2, vlen, 8, ld)

#define epsilon 5

#define VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, ebyte, ldins, fmask) \
    li a4, vlen;    \
    la a5, vec1;    \
    la a6, vec2;    \
  1:                \
    ldins t0, 0(a5);   \
    ldins t1, 0(a6);   \
    andi t0, t0, fmask; \
    andi t1, t1, fmask; \
    sub t0, t0, t1; \
    srai t1, t0, 31; \
    add t0, t0, t1; \
    xor t0, t0, t1; \
    li t1, epsilon ; \
    bgt t0, t1, fail; \
    addi a5, a5, ebyte;  \
    addi a6, a6, ebyte;  \
    addi a4, a4, -1;    \
    bnez a4, 1b;        \

// check if equal on two vectors with float elements
#define VV_HF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_HF_DEFAULT(vec1, vec2, vlen)
#define VV_SF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, 4, lw, 0x7fffff)
#define VV_DF_CHECK_EQ(vec1, vec2, vlen) VV_CHECK_EQ_F_INTERNAL(vec1, vec2, vlen, 8, ld, 0xfffffffffffff)

#-----------------------------------------------------------------------
# Tests for .vv instructions
# mask:
#            0   enable mask
#            1   disable mask
# val0:
#           when disable mask, this can be anything;
#           when enable mask, this is value of v0.t
#-----------------------------------------------------------------------
#define TEST_V_VV_OP2_INTERNAL( testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, mask, val0, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, val2 ; \
    la a5, val0; \
    la a3, test_ ## testnum ## _data ; \
1: \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
    ldins v2, (a2); \
    add a2, a2, t0; \
    ldins v0, (a5); \
    ldins v3, (a5); \
    add a5, a5, t0; \
    vfsub.vv v3, v3, v3; \
    inst v3, v2, v1 VM_ ## mask ## ; \
    stins v3, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_VV_SB_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 8, vlb.v, vsb.v, mask, val0, VV_SB_CHECK_EQ)

#define TEST_V_VV_SH_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, mask, val0, VV_SH_CHECK_EQ)

#define TEST_V_VV_SW_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, mask, val0, VV_SW_CHECK_EQ)

#define TEST_V_VV_SD_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, mask, val0, VV_SD_CHECK_EQ)

#define TEST_V_VV_HF_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, mask, val0, VV_HF_CHECK_EQ)

#define TEST_V_VV_SF_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, mask, val0, VV_SF_CHECK_EQ)

#define TEST_V_VV_DF_OP2( testnum, inst, result, val1, val2, vlen, mask, val0) \
  TEST_V_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, mask, val0, VV_DF_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for vmXXX.vv instructions
# mask:
#            0   enable mask
#            1   disable mask
# val0:
#           when disable mask, this can be anything;
#           when enable mask, this is value of v0.t
# vld:
#            when its vfmXXX instruction, this can be anything;
#            when its NOT vfmXXX instruction, this value is vds address;
#
# TODO: mask is conflicts with the vmXXX instructions because vd needs preload
#-----------------------------------------------------------------------
#define TEST_VM_VV_OP2_INTERNAL( testnum, inst, result, val1, val2, vald, vlen, ebits, ldins, stins, mask, val0, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, val2 ; \
    la a3, test_ ## testnum ## _data ; \
    la a7, vald ; \
1: \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
    ldins v2, (a2); \
    add a2, a2, t0; \
    ldins v3, (a7); \
    add a7, a7, t0; \
    la a5, val0; \
    ldins v0, (a5); \
    la a6, vald; \
    ldins v3, (a6); \
    inst v3, v1, v2 VM_ ## mask ## ; \
    stins v3, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_VM_VV_HF_OP2( testnum, inst, result, val1, val2, vld, vlen, mask, val0) \
  TEST_VM_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vld, vlen, 16, vlh.v, vsh.v, mask, val0, VV_HF_CHECK_EQ)

#define TEST_VM_VV_SF_OP2( testnum, inst, result, val1, val2, vld, vlen, mask, val0) \
  TEST_VM_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vld, vlen, 32, vlw.v, vsw.v, mask, val0, VV_SF_CHECK_EQ)

#define TEST_VM_VV_DF_OP2( testnum, inst, result, val1, val2, vld ,vlen, mask, val0) \
  TEST_VM_VV_OP2_INTERNAL(testnum, inst, result, val1, val2, vld, vlen, 64, vle.v, vse.v, mask, val0, VV_DF_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .vi instructions
#-----------------------------------------------------------------------
#define TEST_V_VI_OP2_INTERNAL( testnum, inst, result, imm, val2, vlen, mask, val0, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val2 ; \
    la a3, test_ ## testnum ## _data ; \
    la a4, val0 ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
  ldins v0, (a4) ; \
    add a4, a4, t0; \
  vfsub.vv v2, v2, v2; \
  inst v2, v1, imm VM_ ## mask ## ; \
  stins v2, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_VI_SB_OP2( testnum, inst, result, imm, val2, vlen, mask, val0) \
  TEST_V_VI_OP2_INTERNAL(testnum, inst, result, imm, val2, vlen, mask, val0, 8, vlb.v, vsb.v, VV_SB_CHECK_EQ)

#define TEST_V_VI_SH_OP2( testnum, inst, result, imm, val2, vlen, mask, val0) \
  TEST_V_VI_OP2_INTERNAL(testnum, inst, result, imm, val2, vlen, mask, val0, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#define TEST_V_VI_SW_OP2( testnum, inst, result, imm, val2, vlen, mask, val0) \
  TEST_V_VI_OP2_INTERNAL(testnum, inst, result, imm, val2, vlen, mask, val0, 32, vlw.v, vsw.v, VV_SW_CHECK_EQ)

#define TEST_V_VI_SD_OP2( testnum, inst, result, imm, val2, vlen, mask, val0) \
  TEST_V_VI_OP2_INTERNAL(testnum, inst, result, imm, val2, vlen, mask, val0, 64, vle.v, vse.v, VV_SD_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .vx instructions
#-----------------------------------------------------------------------
#define TEST_V_VX_OP2_INTERNAL( testnum, inst, result, val1, val2, val0, mask ,vlen, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    li a1, val1 ; \
    la a2, val2 ; \
    la a3, test_ ## testnum ## _data ; \
    la a4, val0 ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a2) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a2, a2, t0; \
  ldins v0, (a4) ; \
  add a4, a4, t0; \
  vfsub.vv v2, v2, v2; \
  inst v2, v1, a1 VM_ ## mask ## ; \
  stins v2, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_VX_SB_OP2( testnum, inst, result, val1, val2 ,vlen ,mask, val0) \
  TEST_V_VX_OP2_INTERNAL(testnum, inst, result, val1, val2, val0, mask, vlen, 8, vlb.v, vsb.v, VV_SB_CHECK_EQ)

#define TEST_V_VX_SH_OP2( testnum, inst, result, val1, val2 ,vlen ,mask, val0) \
  TEST_V_VX_OP2_INTERNAL(testnum, inst, result, val1, val2, val0, mask, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#define TEST_V_VX_SW_OP2( testnum, inst, result, val1, val2, vlen, mask ,val0 ) \
  TEST_V_VX_OP2_INTERNAL(testnum, inst, result, val1, val2, val0, mask ,vlen, 32, vlw.v, vsw.v, VV_SW_CHECK_EQ)

#define TEST_V_VX_SD_OP2( testnum, inst, result, val1, val2, vlen, mask ,val0) \
  TEST_V_VX_OP2_INTERNAL(testnum, inst, result, val1, val2, val0, mask ,vlen ,64, vle.v, vse.v, VV_SD_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .vf instructions
#-----------------------------------------------------------------------
#define TEST_V_VF_OP2_INTERNAL( testnum, inst, result, val1, val2, vlen, ebits, vldins, vstins, fldins, eqm, mask, val0) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1; \
    la a2, val2 ; \
    la a5, val0 ; \
    la a3, test_ ## testnum ## _data ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  fldins fa1, (a1) ; \
  vldins v1, (a2) ; \
  vldins v0, (a5) ; \
  vldins v2, (a5) ; \
  vfsub.vv v2, v2, v2 ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a2, a2, t0; \
    beqz s2, 2f; \
    vldins v3, (a7); \
    add a7, a7, t0; \
2: \
  inst v2, v1, fa1 VM_ ## mask ## ; \
  vstins v2, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_VF_HF_OP2( testnum, inst, result, val1, val2, vlen ,mask, val0) \
  TEST_V_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, flw, VV_HF_CHECK_EQ, mask, val0)

#define TEST_V_VF_SF_OP2( testnum, inst, result, val1, val2, vlen ,mask, val0) \
  TEST_V_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, flw, VV_SF_CHECK_EQ, mask, val0)

#define TEST_V_VF_DF_OP2( testnum, inst, result, val1, val2, vlen ,mask, val0) \
  TEST_V_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, fld, VV_DF_CHECK_EQ, mask, val0)

#-----------------------------------------------------------------------
# Tests for vmXXX.vf instructions
#-----------------------------------------------------------------------
#define TEST_VM_VF_OP2_INTERNAL( testnum, inst, result, val1, val2, vald, vlen, ebits, vldins, vstins, fldins, eqm, mask, val0) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1; \
    la a2, val2 ; \
    la a3, test_ ## testnum ## _data ; \
    la a7, vald ; \
    la a6, val0 ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  fldins fa1, (a1) ; \
  vldins v1, (a2) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a2, a2, t0; \
    vldins v2, (a7); \
    add a7, a7, t0; \
    vldins v0, (a6); \
    add a6, a6, t0; \
2: \
  inst v2, fa1, v1 VM_ ## mask ## ; \
  vstins v2, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_VM_VF_HF_OP2( testnum, inst, result, val1, val2, vald, vlen ,mask, val0) \
   TEST_VM_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vald, vlen, 16, vlh.v, vsh.v, flw, VV_HF_CHECK_EQ, mask, val0)

#define TEST_VM_VF_SF_OP2( testnum, inst, result, val1, val2, vald, vlen ,mask, val0) \
   TEST_VM_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vald, vlen, 32, vlw.v, vsw.v, flw, VV_SF_CHECK_EQ, mask, val0)

#define TEST_VM_VF_DF_OP2( testnum, inst, result, val1, val2, vald, vlen ,mask, val0) \
   TEST_VM_VF_OP2_INTERNAL(testnum, inst, result, val1, val2, vald, vlen, 64, vle.v, vse.v, fld, VV_DF_CHECK_EQ, mask, val0)

#-----------------------------------------------------------------------
# Tests for .s.x instructions
#-----------------------------------------------------------------------
#define TEST_V_SX_OP2_INTERNAL( testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    li a2, val2 ; \
    la a3, test_ ## testnum ## _data ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
  inst v0, a2; \
    li a2, 0; \
  stins v0, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_SX_SB_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SX_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 8, vlb.v, vsb.v, VV_SB_CHECK_EQ)

#define TEST_V_SX_SH_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SX_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#define TEST_V_SX_SW_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SX_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, VV_SW_CHECK_EQ)

#define TEST_V_SX_SD_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SX_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, VV_SD_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .f.s instructions
#-----------------------------------------------------------------------
#define TEST_V_FS_OP2_INTERNAL( testnum, inst, result, val1, vlen, ebits, ldins, stins, fstins, xldins ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, result; \
    la a3, test_ ## testnum ## _data; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a1) ; \
  inst fa1, v0; \
    fstins fa1, (a3) ; \
    xldins t0, 0(a3);   \
    xldins t1, 0(a2);   \
    bne t0, t1, fail;   \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill 1, (ebits/8), 0; \
    .popsection

#define TEST_V_FS_SF_OP2( testnum, inst, result, val1, vlen ) \
  TEST_V_FS_OP2_INTERNAL(testnum, inst, result, val1, vlen, 32, vlw.v, vsw.v, fsw, lw)

#define TEST_V_FS_DF_OP2( testnum, inst, result, val1, vlen ) \
  TEST_V_FS_OP2_INTERNAL(testnum, inst, result, val1, vlen, 64, vle.v, vse.v, fsd, ld)

#-----------------------------------------------------------------------
# Tests for vfirst instructions
#-----------------------------------------------------------------------
#define TEST_V_POP_OP2_INTERNAL( testnum, inst, result, val1, v0t, vlen, mask, ebits, ldins, stins, fstins, xldins) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, result; \
    lw t2, (a2);\
    la a4, v0t ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
  ldins v0, (a4) ; \
  inst t0, v1 VM_ ## mask ## ; \
  la a2, test_ ## testnum ## _data; \
  sw t0, (a2) ; \
  lw t2, (a2) ; \
    bne t0, t2, fail;   \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill 1, (ebits/8), 0; \
    .popsection

#define TEST_V_POP_HF_OP2( testnum, inst, result, val1, v0t, vlen, mask) \
  TEST_V_POP_OP2_INTERNAL(testnum, inst, result, val1, v0t, vlen, mask, 16, vlh.v, vsh.v, fsh, lh)

#define TEST_V_POP_SF_OP2( testnum, inst, result, val1, v0t, vlen, mask) \
  TEST_V_POP_OP2_INTERNAL(testnum, inst, result, val1, v0t, vlen, mask, 32, vlw.v, vsw.v, fsw, lw)

#define TEST_V_POP_DF_OP2( testnum, inst, result, val1, v0t, vlen, mask) \
  TEST_V_POP_OP2_INTERNAL(testnum, inst, result, val1, v0t, vlen, mask, 64, vle.v, vse.v, fsd, ld)
#-----------------------------------------------------------------------
# Tests for .s.f instructions
#-----------------------------------------------------------------------
#define TEST_V_SF_OP2_INTERNAL( testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, fldins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, val2 ; \
    fldins fa1, (a2) ; \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a1) ; \
  inst v0, fa1; \
  stins v0, (a1); \
    eqm(result, val1, vlen);

#define TEST_V_SF_SF_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SF_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, flw, VV_SW_CHECK_EQ)

#define TEST_V_SF_DF_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_SF_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, fld, VV_SD_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for cvt instructions
#-----------------------------------------------------------------------
#define TEST_V_CVT_W_S_OP1_INTERNAL( testnum, inst, result, val1, vlen, mask, val0, ebits, ldins, stins, fldins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a3, test_ ## testnum ## _data; \
    la a4, val0; \
1: \
  vsetvli t0, a0, e ## ebits; \
  ldins v1, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
  ldins v0, (a4) ; \
    add a4, a4, t0; \
  vfsub.vv v2, v2, v2; \
  inst v2, v1 VM_ ## mask ## ; \
  stins v2, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_CVT_H_S_OP1( testnum, inst, result, val1, vlen, mask, val0 ) \
  TEST_V_CVT_W_S_OP1_INTERNAL(testnum, inst, result, val1, vlen, mask, val0, 16, vlh.v, vsh.v, flw, VV_SH_CHECK_EQ)

#define TEST_V_CVT_W_S_OP1( testnum, inst, result, val1, vlen, mask, val0) \
  TEST_V_CVT_W_S_OP1_INTERNAL(testnum, inst, result, val1, vlen, mask, val0, 32, vlw.v, vsw.v, flw, VV_SW_CHECK_EQ)

#define TEST_V_CVT_D_S_OP1( testnum, inst, result, val1, vlen, mask, val0 ) \
  TEST_V_CVT_W_S_OP1_INTERNAL(testnum, inst, result, val1, vlen, mask, val0, 64, vle.v, vse.v, fld, VV_SD_CHECK_EQ)

#-----------------------------------------------------------------------
# Tests for .v instructions
#-----------------------------------------------------------------------
#define TEST_V_V_OP1_INTERNAL( testnum, inst, result, val1, vlen, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a3, test_ ## testnum ## _data ; \
1: \
  vsetvli t0, a0, e ## ebits; \
  ldins v0, (a1) ; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
    add a1, a1, t0; \
  inst v1, v0; \
  stins v1, (a3); \
    add a3, a3, t0; \
    bnez a0, 1b; \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_V_HF_OP1( testnum, inst, result, val1, vlen ) \
  TEST_V_V_OP1_INTERNAL(testnum, inst, result, val1, vlen, 16, vlh.v, vsh.v, VV_HF_CHECK_EQ)

#define TEST_V_V_SF_OP1( testnum, inst, result, val1, vlen ) \
  TEST_V_V_OP1_INTERNAL(testnum, inst, result, val1, vlen, 32, vlw.v, vsw.v, VV_SF_CHECK_EQ)

#define TEST_V_V_DF_OP1( testnum, inst, result, val1, vlen ) \
  TEST_V_V_OP1_INTERNAL(testnum, inst, result, val1, vlen, 64, vle.v, vse.v, VV_DF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for .vs instructions
#-----------------------------------------------------------------------
#define TEST_V_VS_OP2_INTERNAL( testnum, inst, result, val1, val2, vlen, ebits, ldins, stins, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    la a2, val2 ; \
    la a3, test_ ## testnum ## _data ; \
  vsetvli t0, a0, e ## ebits; \
    ldins v0, (a1) ; \
    ldins v2, (a3) ; \
1: \
  vsetvli t0, a0, e ## ebits; \
    sub a0, a0, t0; \
    slli t0, t0, VSHIFT ## ebits; \
  ldins v1, (a2); \
    add a2, a2, t0; \
  inst v0, v1, v0; \
    bnez a0, 1b; \
    li a0, 1; \
  vsetvli t0, a0, e ## ebits; \
    stins v0, (a3); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#define TEST_V_VS_SB_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 8, vlb.v, vsb.v, VV_SB_CHECK_EQ)

#define TEST_V_VS_SH_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_SH_CHECK_EQ)

#define TEST_V_VS_SW_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, VV_SW_CHECK_EQ)

#define TEST_V_VS_SD_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, VV_SD_CHECK_EQ)

#define TEST_V_VS_HF_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 16, vlh.v, vsh.v, VV_HF_CHECK_EQ)

#define TEST_V_VS_SF_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 32, vlw.v, vsw.v, VV_SF_CHECK_EQ)

#define TEST_V_VS_DF_OP2( testnum, inst, result, val1, val2, vlen ) \
  TEST_V_VS_OP2_INTERNAL(testnum, inst, result, val1, val2, vlen, 64, vle.v, vse.v, VV_DF_CHECK_EQ)


#-----------------------------------------------------------------------
# Tests for  vector load instructions, not support vlen multiplicate
#-----------------------------------------------------------------------
#define TEST_VLOAD_OP1_INTERNAL( testnum, ldins, stins, result, val1, vlen, ebits, mask, val0, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    addi a2, x0, mask;\
    la a3, test_ ## testnum ## _data ; \
1: \
    vsetvli t0, a0, e ## ebits; \
    beqz a2, 2f; \
    ldins v1, (a1) ; \
    j 3f; \
2: \
    la a4, val0; \
    ldins v0, (a4); \
    la a5, result; \
    ldins v1, (a5); \
    ldins v1, (a1), v0.t; \
3: \
    stins v1, (a3); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#-----------------------------------------------------------------------
# Tests for  vector stride load instructions, not support vlen multiplicate
#-----------------------------------------------------------------------
#define TEST_VSLOAD_OP2_INTERNAL( testnum, testins, stride, ldins, stins, result, val1, vlen, ebits, mask, val0, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    addi a2, x0, mask;\
    la a3, test_ ## testnum ## _data ; \
    li a6, stride; \
1: \
    vsetvli t0, a0, e ## ebits; \
    beqz a2, 2f; \
    testins v1, (a1), a6; \
    j 3f; \
2: \
    la a4, val0; \
    ldins v0, (a4); \
    la a5, result; \
    ldins v1, (a5); \
    testins v1, (a1), a6, v0.t; \
3: \
    stins v1, (a3); \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#-----------------------------------------------------------------------
# Tests for  vector store instructions, not support vlen multiplicate
#-----------------------------------------------------------------------
#define TEST_VSTORE_OP1_INTERNAL( testnum, ldins, stins, result, val1, vlen, ebits, mask, val0, eqm ) \
test_ ## testnum: \
    li TESTNUM, testnum; \
    li a0, vlen ; \
    la a1, val1 ; \
    addi a2, x0, mask;\
    la a3, test_ ## testnum ## _data ; \
1: \
    vsetvli t0, a0, e ## ebits; \
    ldins v1, (a1) ; \
    beqz a2, 2f; \
    stins v1, (a3); \
    j 3f; \
2: \
    la a4, val0; \
    ldins v0, (a4); \
    stins v1, (a3), v0.t; \
3: \
    eqm(result, test_ ## testnum ## _data, vlen); \
    .pushsection .data; \
test_ ## testnum ## _data: \
    .fill vlen, (ebits/8), 0; \
    .popsection

#endif
