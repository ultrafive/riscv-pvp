#ifndef __TEST_MACROS_MECONV_H
#define __TEST_MACROS_MECONV_H

#include "test_macros_stc.h"
#include "exception.h"

#define MECONV_RD_ADDR   IMB_ADDR
#define MECONV_RS1_ADDR  0xc0000000
#define MECONV_RS2_ADDR  0xc0080000

#-----------------------------------------------------------------------
# Tests for meconv.mm instructions
#-----------------------------------------------------------------------

/* Select different macros based on element type */
#if defined(HF)
  #define INST meconv.mm
  #define ESIZE_IN 2
  #define ESIZE_OUT 2
  #define LDINS lh
  #define STINS sh
  #define LDOUTS lh
  #define STOUTS sh
  #define SET_DEQUANT_CSR(testnum)
  #define VV_CHECK_EQ(a1, a2, len, acc) \
      VV_CHECK_EQ_HF_ACC(a1, a2, len, 0.005, 1, acc)
#elif defined(X8)
  #define INST meconv.x8.mm
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
  #define INST meconv.hf.x8.mm
  #define ESIZE_IN 1
  #define ESIZE_OUT 2
  #define LDINS lb
  #define STINS sb
  #define LDOUTS lh
  #define STOUTS sh
  #define SET_DEQUANT_CSR(testnum) \
      la t0, t##testnum##_dequant; \
      lw t0, 0(t0); \
      csrw conv_dequant_coeff, t0;
  #define VV_CHECK_EQ(a1, a2, len, acc) \
      VV_CHECK_EQ_HF(a1, a2, len, 0.0001, 2)
#else
  #error "unexpected element type"
#endif

#define SETCSR(h, w, cin, cout, kh, kw, out_h, out_w, pt, pb, pl, pr, sk, dl, stride_s1, stride_s2, stride_d) \
  li t0, ((w << 16) | h); \
  csrw conv_FM_in, t0; \
  li t0, ((out_w << 16) | out_h); \
  csrw conv_FM_out, t0; \
  li t0, ((stride_s1 << 16) | cin); \
  csrw conv_Depth_in, t0; \
  li t0, ((stride_d << 16) | cout); \
  csrw conv_Depth_out, t0; \
  li t0, stride_s2; \
  csrw conv_S_kernel, t0; \
  li t0, ((kw << 24) | (kh << 16) | (dl << 8) | sk); \
  csrw conv_kernel, t0; \
  li t0, ((pt << 24) | (pb << 16) | (pl << 8) | pr); \
  csrw conv_padding, t0;

/* Invoke MME instruction */
#define MECONV(rd, rs1, rs2) \
  INST (rd), (rs1), (rs2)

/* Copy data in to a strided input */
#define COPY_IN_STRIDE COPY_STRIDE_D

/* Copy data out from a strided output */
#define COPY_OUT_STRIDE COPY_STRIDE_S

/* Test conv2d(val1, val2) and compare it with result. */
#define TEST_MECONV_PADDING_SK_DILATION(testnum, result, val1, val2, h, w, cin, cout, kh, kw, out_h, out_w, pt, pb, pl, pr, sk, dl) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(MECONV_RS1_ADDR, val1, h * w * cin, LDINS, STINS, ESIZE_IN) \
  COPY(MECONV_RS2_ADDR, val2, kh * kw * cin * cout, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, cin, cout, kh, kw, out_h, out_w, pt, pb, pl, pr, sk, dl, 0, 0, 0) \
  SET_DEQUANT_CSR(testnum) \
  PERF_BEGIN() \
  la a0, MECONV_RD_ADDR; \
  la a1, MECONV_RS1_ADDR; \
  la a2, MECONV_RS2_ADDR; \
  MECONV(a0, a1, a2); \
  PERF_END(w ## _ ## h ## _ ## cin ## _ ## cout ## _ ## kw ## _ ## kh ## _ ## testnum) \
  \
  COPY(test_##testnum##_data, MECONV_RD_ADDR, out_h * out_w * cout, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, out_h * out_w * cout, cin * kh * kw) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill out_h * out_w * cout, ESIZE_OUT, 0; \
  .popsection

#define TEST_MECONV(testnum, result, val1, val2, h, w, cin, cout, kh, kw, out_h, out_w) \
  TEST_MECONV_PADDING_SK_DILATION(testnum, result, val1, val2, h, w, cin, cout, kh, kw, out_h, out_w, 0, 0, 0, 0, 1, 1)

/* Test meconv with memory strides on operands */
#define TEST_MECONV_STRIDE(testnum, result, val1, val2, h, w, cin, cout, kh, kw, out_h, out_w, stride_s1, stride_s2, stride_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY_IN_STRIDE(MECONV_RS1_ADDR, val1, h * w, cin, stride_s1, LDINS, STINS, ESIZE_IN) \
  COPY_IN_STRIDE(MECONV_RS2_ADDR, val2, kh * kw * cin, cout, stride_s2, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, cin, cout, kh, kw, out_h, out_w, 0, 0, 0, 0, 1, 1, stride_s1, stride_s2, stride_d) \
  SET_DEQUANT_CSR(testnum) \
  la a0, MECONV_RD_ADDR; \
  la a1, MECONV_RS1_ADDR; \
  la a2, MECONV_RS2_ADDR; \
  MECONV(a0, a1, a2); \
  \
  COPY_OUT_STRIDE(test_##testnum##_data, MECONV_RD_ADDR, out_h * out_w, cout, stride_d, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, out_h * out_w * cout, cin * kh * kw) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill out_h * out_w * cout, ESIZE_OUT, 0; \
  .popsection

/* Test matmul with misaligned address of meconv operands */
#define TEST_MECONV_MISALIGNED_BLOCK(testnum, result, val1, val2, h, w, cin, cout, kh, kw, out_h, out_w, off_s1, off_s2, off_d) \
test_ ## testnum: \
  li TESTNUM, testnum; \
  \
  COPY(MECONV_RS1_ADDR+off_s1, val1, h * w * cin, LDINS, STINS, ESIZE_IN) \
  COPY(MECONV_RS2_ADDR+off_s2, val2, kh * kw * cin * cout, LDINS, STINS, ESIZE_IN) \
  \
  SETCSR(h, w, cin, cout, kh, kw, out_h, out_w, 0, 0, 0, 0, 1, 1, 0, 0, 0) \
  SET_DEQUANT_CSR(testnum) \
  la a0, MECONV_RD_ADDR+off_d; \
  la a1, MECONV_RS1_ADDR+off_s1; \
  la a2, MECONV_RS2_ADDR+off_s2; \
  MECONV(a0, a1, a2); \
  \
  COPY(test_##testnum##_data, MECONV_RD_ADDR+off_d, out_h * out_w * cout, LDOUTS, STOUTS, ESIZE_OUT) \
  VV_CHECK_EQ(result, test_ ## testnum ## _data, out_h * out_w * cout, cin * kh * kw) \
  .pushsection .data; \
test_ ## testnum ## _data: \
  .fill out_h * out_w * cout, ESIZE_OUT, 0; \
  .popsection

/* Test element misaligned base addresses */
#define TEST_MECONV_EXCEPTION_MISALIGNED_BASE(testnum, off_s1, off_s2, off_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_BASE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(4, 4, 4, 4, 3, 3, 2, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0) \
  li a0, RD_ADDR + off_d; \
  li a1, RS1_ADDR + off_s1; \
  li a2, RS2_ADDR + off_s2; \
  MECONV(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid parameters */
#define TEST_MECONV_EXCEPTION_INVALID_PARAM(testnum, h, w, cin, cout, kh, kw, out_h, out_w, sk, dl) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_INVALID_PARAM, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(h, w, cin, cout, kh, kw, out_h, out_w, 0, 0, 0, 0, sk, dl, 0, 0, 0); \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  MECONV(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test misaligned strides */
#define TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(testnum, stride_s1, stride_s2, stride_d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_MISALIGNED_STRIDE, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(4, 4, 4, 4, 3, 3, 2, 2, 0, 0, 0, 0, 1, 1, stride_s1, stride_s2, stride_d) \
  li a0, RD_ADDR; \
  li a1, RS1_ADDR; \
  li a2, RS2_ADDR; \
  MECONV(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/* Test invalid access */
#define TEST_MECONV_EXCEPTION_ACCESS_FAULT(testnum, s1, s2, d) \
test_ ## testnum: \
  TEST_EXCEPTION(CAUSE_NCP_CUST_ACCESS, test_ ## testnum ## _end); \
  li TESTNUM, testnum; \
  SETCSR(4, 4, 4, 4, 3, 3, 2, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0) \
  la a0, d; \
  la a1, s1; \
  la a2, s2; \
  MECONV(a0, a1, a2); \
  j fail; \
test_ ## testnum ## _end:

/*****************************/
/*     Test exceptions       */
/*****************************/
// Test misaligned addresses
  // 111: RS1 misaligned
  // 112: RS2 misaligned
  // 113: RD misaligned
  // 114: RS1/RS2/RD misaligned
#ifdef HF
#define TEST_MECONV_EXCEPTION_MISALIGNED_BASE_CASES \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE(111, 31, 0, 0); \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE(112, 0, 71, 0); \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE(113, 0, 0, 55); \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE(114, 73, 59, 13)
#else
#define TEST_MECONV_EXCEPTION_MISALIGNED_BASE_CASES \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE(113, 0, 0, 55)
#endif

// Test misaligned strides
  // 115: RS1 stride misaligned
  // 116: RS2 stride misaligned
  // 117: RD stride misaligned
  // 118: RS1/RS2/RD stride misaligned
  // 119: RD stride < width
#ifdef HF
#define TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE_CASES \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(115, 59, 0, 0); \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(116, 0, 63, 0); \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(117, 0, 0, 49); \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(118, 61, 71, 15); \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(119, 0, 0, 4)
#else
#define TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE_CASES \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(117, 0, 0, 49); \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE(119, 0, 0, 4)
#endif

// Test invalid parameter
  // 120: height == 0
  // 121: width == 0
  // 122: cin == 0
  // 123: cout == 0
  // 124: kh == 0
  // 125: kw == 0
  // 126: sk == 0
  // 127: dl == 0
#define TEST_MECONV_EXCEPTION_INVALID_PARAM_CASES \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(120, 0, 4, 4, 4, 3, 3, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(121, 4, 0, 4, 4, 3, 3, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(122, 4, 4, 0, 4, 3, 3, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(123, 4, 4, 4, 0, 3, 3, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(124, 4, 4, 4, 4, 0, 3, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(125, 4, 4, 4, 4, 3, 0, 2, 2, 1, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(126, 4, 4, 4, 4, 3, 3, 2, 2, 0, 1); \
  TEST_MECONV_EXCEPTION_INVALID_PARAM(127, 4, 4, 4, 4, 3, 3, 2, 2, 1, 0); \

// Test access fault
  // 128: Invalid write to L1 buffer
  // 129: Invalid read rs2 from IM buffer
  // 130: Read rs1 over IM buffer
  // 131: Read rs2 over L1 buffer
  // 132: Write rd over IM buffer
#define TEST_MECONV_EXCEPTION_ACCESS_FAULT_CASES \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT(128, L1B_ADDR, L1B_ADDR+128, L1B_ADDR+256); \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT(129, L1B_ADDR, IMB_ADDR, IMB_ADDR+128); \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT(130, IMB_END-4, L1B_ADDR, IMB_ADDR); \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT(131, L1B_ADDR, L1B_END-4, IMB_ADDR); \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT(132, L1B_ADDR, L1B_ADDR+128, IMB_END-4)

#define TEST_MECONV_EXCEPTION_CASES \
  TEST_MECONV_EXCEPTION_MISALIGNED_BASE_CASES; \
  TEST_MECONV_EXCEPTION_MISALIGNED_STRIDE_CASES; \
  TEST_MECONV_EXCEPTION_INVALID_PARAM_CASES; \
  TEST_MECONV_EXCEPTION_ACCESS_FAULT_CASES
#endif
