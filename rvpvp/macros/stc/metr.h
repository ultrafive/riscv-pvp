#ifndef __TEST_MACROS_METR_H
#define __TEST_MACROS_METR_H

#include "test_macros_stc.h"
#include "exception.h"

#define METR_RD_ADDR   IMB_ADDR
#define METR_RS1_ADDR  0xc0000000

#-----------------------------------------------------------------------
# Tests for metr.m instructions
#-----------------------------------------------------------------------

#define ESIZE_IN 2
#define ESIZE_OUT 2
#define LDINS lh
#define STINS sh
#define LDOUTS lh
#define STOUTS sh
#define VV_CHECK_EQ(a1, a2, len) \
        VV_CHECK_EQ_INT16(a1, a2, len)

#define SETCSR(h, w, stride_s1, stride_d) \
  li t0, (w << 16 + h); \
  csrw m_shape_s1, t0; \
  li t0, stride_s1; \
  csrw m_stride_s, t0; \
  li t0, stride_d; \
  csrw m_stride_d, t0;

/* Copy data in to a strided input */
#define COPY_IN_STRIDE COPY_STRIDE_D

/* Copy data out from a strided output */
#define COPY_OUT_STRIDE COPY_STRIDE_S

/* Test metr(val) and compare it with result.
   val: (h, w) tensor */
#define TEST_METR(testnum, result, val, h, w) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(METR_RS1_ADDR, val, h * w, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, 0, 0) \
  PERF_BEGIN() \
  la a0, METR_RD_ADDR; \
  la a1, METR_RS1_ADDR; \
  metr.m (a0), (a1); \
  PERF_END(w ## _ ## h) \
  \
  COPY(test_##testnum##_data, METR_RD_ADDR, h * w, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, h * w) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill h * w, ESIZE_OUT, 0; \
  .popsection

/* Test transpose with strides on metr operands */
#define TEST_METR_STRIDE(testnum, result, val, h, w, stride_s, stride_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY_IN_STRIDE(METR_RS1_ADDR, val, h, w, stride_s, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, stride_s, stride_d) \
  PERF_BEGIN() \
  la a0, METR_RD_ADDR; \
  la a1, METR_RS1_ADDR; \
  metr.m (a0), (a1); \
  PERF_END(w ## _ ## h ## _ ## stride_s ## _ ## stride_d) \
  \
  COPY_OUT_STRIDE(test_##testnum##_data, METR_RD_ADDR, w, h, stride_d, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, h * w) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill h * w, ESIZE_OUT, 0; \
  .popsection

/* Test block-misaligned (not 128-byte aligned) addresses */
#define TEST_METR_MISALIGNED_BLOCK(testnum, result, val, h, w, off_s, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(METR_RS1_ADDR+off_s, val, h * w, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, 0, 0) \
  la a0, METR_RD_ADDR+off_d; \
  la a1, METR_RS1_ADDR+off_s; \
  metr.m (a0), (a1); \
  \
  COPY(test_##testnum##_data, METR_RD_ADDR+off_d, h * w, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, h * w) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill h * w, ESIZE_OUT, 0; \
  .popsection

/* Test element misaligned base addresses */
#define TEST_METR_EXCEPTION_MISALIGNED_BASE(testnum, h, w, off_s, off_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(h, w, 0, 0) \
  li a0, RD_ADDR + off_d; \
  li a1, RS1_ADDR + off_s; \
  metr.m (a0), (a1); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid parameters */
#define TEST_METR_EXCEPTION_INVALID_PARAM(testnum, h, w) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(h, w, 0, 0) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  metr.m (a0), (a1); \
  j fail; \
test_ ## testnum ## _end:

/* Test misaligned strides */
#define TEST_METR_EXCEPTION_MISALIGNED_STRIDE(testnum, h, w, stride_s, stride_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(h, w, stride_s, stride_d) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  metr.m (a0), (a1); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid access */
#define TEST_METR_EXCEPTION_ACCESS_FAULT(testnum, h, w, s, d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(h, w, 0, 0) \
  la a0, d; \
  la a1, s; \
  metr.m (a0), (a1); \
  j fail; \
test_ ## testnum ## _end:

#endif
