// See LICENSE for license details.

#ifndef __TEST_MACROS_EXCEPTION_H
#define __TEST_MACROS_EXCEPTION_H

#define TEST_EXCEPTION( cause_code, restore_addr ) \
    la t0, cause_code; \
    la t1, _expected_cause; \
    sw t0, 0(t1); \
    la t0, restore_addr; \
    la t1, _restore_addr; \
    sw t0, 0(t1); \


#define TEST_EXCEPTION_HANDLER \
    .align 2; \
mtvec_handler: \
    la t1, _expected_cause; \
    lw t2, 0(t1); \
    csrr t0, mcause; \
    bne t0, t2, fail; \
    \
    la t0, _restore_addr; \
    ld t1, 0(t0); \
    jr t1; \
    .pushsection .data; \
    .align 4; .global _expected_cause; _expected_cause: .dword 0; \
    .align 4; .global _restore_addr; _restore_addr: .dword 0; \
    .popsection; \

#endif
