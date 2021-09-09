// See LICENSE for license details.

#ifndef __TEST_MACROS_VECTOR_H
#define __TEST_MACROS_VECTOR_H

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


#endif
