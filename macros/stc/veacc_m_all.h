// See LICENSE for license details.

#ifndef __TEST_MACROS_VEACC_M_ALL_H
#define __TEST_MACROS_VEACC_M_ALL_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#define FP_CHECK_EQ(fp0, fp1, acc) \
    fclass.s t0 , fp1; \
    li t1, 0x200; \
    beq t0, t1, 89f; \
    feq.s t0, fp0, fp1; \
    bnez t0, 91f; \
    fsub.s fp0, fp0, fp1; \
    fabs.s fp0, fp0; \
    la a0, 92f; \
    flw ft0, 0(a0); \
    li t0, acc; \
    fcvt.s.w ft1, t0; \
    fmul.s ft0, ft1, ft0; \
    flt.s t0, fp0, ft0; \
    bnez t0, 91f; \
    j fail; \
  89:\
    fclass.s t0, fp0; \
    beq t0, t1, 91f; \
    j fail; \
  91: \
    .pushsection .data; \
  92: \
    .float 0.5; \
    .popsection

#include "vexxx_m_all.h"

#endif
