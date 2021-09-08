#ifndef __TEST_MACROS_MEMUL_H
#define __TEST_MACROS_MEMUL_H

#include "test_macros_stc.h"
#include "exception.h"

#define MEMUL_RD_ADDR   IMB_ADDR
#define MEMUL_RS1_ADDR  0xc0000000
#define MEMUL_RS2_ADDR  0xc0080000

#-----------------------------------------------------------------------
# Tests for memul.mm instructions
#-----------------------------------------------------------------------

/* Select different macros based on element type */
#if defined(HF)
  #define INST memul.mm
  #define ESIZE_IN 2
  #define ESIZE_OUT 2
  #define LDINS lh
  #define STINS sh
  #define LDOUTS lh
  #define STOUTS sh
  #define SET_DEQUANT_CSR(testnum)
  #define VV_CHECK_EQ(a1, a2, len, acc) \
      VV_CHECK_EQ_HF_ACC(a1, a2, len, 0.0005, 1, acc)
#elif defined(X8)
  #define INST memul.x8.mm
  #define ESIZE_IN 1
  #define ESIZE_OUT 4
  #define LDINS lb
  #define STINS sb
  #define LDOUTS lw
  #define STOUTS sw
  #define SET_DEQUANT_CSR(testnum)
  #define VV_CHECK_EQ(a1, a2, len, acc) \
      VV_CHECK_EQ_INT32(a1, a2, len)
#elif defined(HF_X8)
  #define INST memul.hf.x8.mm
  #define ESIZE_IN 1
  #define ESIZE_OUT 2
  #define LDINS lb
  #define STINS sb
  #define LDOUTS lh
  #define STOUTS sh
  #define SET_DEQUANT_CSR(testnum) \
      la t0, test_dequant;/*t##testnum##_dequant;*/ \
      lw t0, 0(t0); \
      csrw m_dequant_coeff, t0;
  #define VV_CHECK_EQ(a1, a2, len, acc) \
      VV_CHECK_EQ_HF(a1, a2, len, 0.0001, 2)
#else
  #error "unexpected element type"
#endif

/* Set shapes and strides */
#ifdef TS
#define SHAPE_S1(m, k) (m << 16 + k)
#else
#define SHAPE_S1(m, k) (k << 16 + m)
#endif

#define SETCSR(m, k, n, stride_s1, stride_s2, stride_d) \
  li a0, SHAPE_S1(m, k); \
  li a1, (n << 16 + k); \
  csrw m_shape_s1, a0; \
  csrw m_shape_s2, a1; \
  li a0, (stride_s2 << 16 + stride_s1); \
  li a1, stride_d; \
  csrw m_stride_s, a0; \
  csrw m_stride_d, a1;

/* Invoke MME instruction */
#ifdef TS
#define MEMUL(rd, rs1, rs2) \
  INST (rd), (rs1), (rs2), ts
#else
#define MEMUL(rd, rs1, rs2) \
  INST (rd), (rs1), (rs2)
#endif

/* Copy data in to a strided input */
#ifdef TS
#define COPY_IN_STRIDE_S1(dst, src, height, width, stride, ldins, stins, esize) \
  COPY_STRIDE_D(dst, src, width, height, stride, ldins, stins, esize)
#else
#define COPY_IN_STRIDE_S1 COPY_STRIDE_D
#endif
#define COPY_IN_STRIDE_S2 COPY_STRIDE_D

/* Copy data out from a strided output */
#define COPY_OUT_STRIDE COPY_STRIDE_S

/* Test matmul(val1, val2) and compare it with result.
   val1: (m, k) tensor, val2: (k, n) tensor. */
#define TEST_MEMUL(testnum, result, val1, val2, m, k, n) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(MEMUL_RS1_ADDR, val1, m * k, LDINS, STINS, ESIZE_IN) \
  COPY(MEMUL_RS2_ADDR, val2, k * n, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(m, k, n, 0, 0, 0) \
  SET_DEQUANT_CSR(testnum) \
  PERF_BEGIN() \
  la a0, MEMUL_RD_ADDR; \
  la a1, MEMUL_RS1_ADDR; \
  la a2, MEMUL_RS2_ADDR; \
  MEMUL(a0, a1, a2); \
  PERF_END(m ## _ ## k ## _ ## n ## _ ## testnum) \
  \
  COPY(test_##testnum##_data, MEMUL_RD_ADDR, m * n, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, m * n, k) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill m * n, ESIZE_OUT, 0; \
  .popsection

/* Test matmul with strides on memul operands */
#define TEST_MEMUL_STRIDE(testnum, result, val1, val2, m, k, n, stride_s1, stride_s2, stride_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY_IN_STRIDE_S1(MEMUL_RS1_ADDR, val1, m, k, stride_s1, LDINS, STINS, ESIZE_IN) \
  COPY_IN_STRIDE_S2(MEMUL_RS2_ADDR, val2, k, n, stride_s2, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(m, k, n, stride_s1, stride_s2, stride_d) \
  SET_DEQUANT_CSR(testnum) \
  PERF_BEGIN() \
  la a0, MEMUL_RD_ADDR; \
  la a1, MEMUL_RS1_ADDR; \
  la a2, MEMUL_RS2_ADDR; \
  MEMUL(a0, a1, a2); \
  PERF_END(m ## _ ## k ## _ ## n ## _ ## stride_s1 ## _ ## stride_s2 ## _ ## stride_d) \
  \
  COPY_OUT_STRIDE(test_##testnum##_data, MEMUL_RD_ADDR, m, n, stride_d, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, m * n, k) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill m * n, ESIZE_OUT, 0; \
  .popsection

/* Test block-misaligned (not 128-byte aligned) addresses */
#define TEST_MEMUL_MISALIGNED_BLOCK(testnum, result, val1, val2, m, k, n, off_s1, off_s2, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(MEMUL_RS1_ADDR+off_s1, val1, m * k, LDINS, STINS, ESIZE_IN) \
  COPY(MEMUL_RS2_ADDR+off_s2, val2, k * n, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(m, k, n, 0, 0, 0) \
  SET_DEQUANT_CSR(testnum) \
  la a0, MEMUL_RD_ADDR+off_d; \
  la a1, MEMUL_RS1_ADDR+off_s1; \
  la a2, MEMUL_RS2_ADDR+off_s2; \
  MEMUL(a0, a1, a2); \
  \
  COPY(test_##testnum##_data, MEMUL_RD_ADDR+off_d, m * n, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, m * n, k) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill m * n, ESIZE_OUT, 0; \
  .popsection

/* Test element misaligned base addresses */
#define TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(testnum, m, k, n, off_s1, off_s2, off_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(m, k, n, 0, 0, 0) \
  li a0, RD_ADDR + off_d; \
  li a1, RS1_ADDR + off_s1; \
  li a2, RS2_ADDR + off_s2; \
  MEMUL(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid parameters */
#define TEST_MEMUL_EXCEPTION_INVALID_PARAM(testnum, m, k, n) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(m, k, n, 0, 0, 0) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  MEMUL(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test misaligned strides */
#define TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(testnum, m, k, n, stride_s1, stride_s2, stride_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(m, k, n, stride_s1, stride_s2, stride_d) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  MEMUL(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid access */
#define TEST_MEMUL_EXCEPTION_ACCESS_FAULT(testnum, m, k, n, s1, s2, d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(m, k, n, 0, 0, 0) \
  la a0, d; \
  la a1, s1; \
  la a2, s2; \
  MEMUL(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/*****************************/
/*     Test exceptions       */
/*****************************/
// Test misaligned addresses
  // 101: RS1 misaligned
  // 102: RS2 misaligned
  // 103: RD misaligned
  // 104: RS1/RS2/RD misaligned
#ifdef HF
#define TEST_MEMUL_EXCEPTION_MISALIGNED_BASE_CASES \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(101, 1, 1, 1, 31, 0, 0); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(102, 1, 1, 1, 0, 71, 0); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(103, 1, 1, 1, 0, 0, 55); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(104, 1, 1, 1, 73, 59, 13)
#else
#define TEST_MEMUL_EXCEPTION_MISALIGNED_BASE_CASES \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE(103, 1, 1, 1, 0, 0, 55)
#endif

// Test misaligned strides
  // 105: RS1 stride misaligned
  // 106: RS2 stride misaligned
  // 107: RD stride misaligned
  // 108: RS1/RS2/RD stride misaligned
  // 109: RD stride < width
#ifdef HF
#define TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE_CASES \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(105, 2, 2, 2, 59, 0, 0); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(106, 2, 2, 2, 0, 63, 0); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(107, 2, 2, 2, 0, 0, 49); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(108, 2, 2, 2, 61, 71, 15); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(109, 2, 2, 8, 61, 71, 2)
#else
#define TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE_CASES \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(107, 2, 2, 2, 0, 0, 49); \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE(109, 2, 2, 8, 61, 71, 2)
#endif

// Test invalid parameter
  // 110: m == 0
  // 111: k == 0
  // 112: n == 0
  // 113: m == k == n == 0
#define TEST_MEMUL_EXCEPTION_INVALID_PARAM_CASES \
  TEST_MEMUL_EXCEPTION_INVALID_PARAM(110, 0, 1, 1); \
  TEST_MEMUL_EXCEPTION_INVALID_PARAM(111, 1, 0, 1); \
  TEST_MEMUL_EXCEPTION_INVALID_PARAM(112, 1, 1, 0); \
  TEST_MEMUL_EXCEPTION_INVALID_PARAM(113, 0, 0, 0); \

// Test access fault
  // 115: Invalid write to L1 buffer
  // 116: Invalid read rs2 from IM buffer
  // 117: Read rs1 over IM buffer
  // 118: Read rs2 over L1 buffer
  // 119: Write rd over IM buffer
#define TEST_MEMUL_EXCEPTION_ACCESS_FAULT_CASES \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT(115, 1, 1, 1, L1B_ADDR, L1B_ADDR+128, L1B_ADDR+256); \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT(116, 1, 1, 1, L1B_ADDR, IMB_ADDR, IMB_ADDR+128); \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT(117, 4, 4, 4, IMB_END-4, L1B_ADDR, IMB_ADDR); \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT(118, 4, 4, 4, L1B_ADDR, L1B_END-4, IMB_ADDR); \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT(119, 4, 4, 4, L1B_ADDR, L1B_ADDR+128, IMB_END-4)

#define TEST_MEMUL_EXCEPTION_CASES \
  TEST_MEMUL_EXCEPTION_MISALIGNED_BASE_CASES; \
  TEST_MEMUL_EXCEPTION_MISALIGNED_STRIDE_CASES; \
  TEST_MEMUL_EXCEPTION_INVALID_PARAM_CASES; \
  TEST_MEMUL_EXCEPTION_ACCESS_FAULT_CASES
#endif
