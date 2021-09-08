#ifndef __TEST_MACROS_CHECK_EQ_H
#define __TEST_MACROS_CHECK_EQ_H

// The absolute torlance, for float16, the atol is 1e0-4
#define VV_CHECK_EQ_HF_ATOL 0.0001
// The relative torlance as binary comparsion for two float16 number
#define VV_CHECK_EQ_HF_RTOL 1

/*************************************************************************/
/* Function vv_check_eq_hf: check if two FP16 vectors are compared equal */
/* Return value: 0: all FP16 values compared equal                       */
/*               1: compared fail                                        */
/* Argument a0: vector 1 address                                         */
/* Argument a1: vector 2 address                                         */
/* Argument a2: number of elements                                       */
/* Argument a3: relative epsilon - indicates the maximum accetable       */
/*              difference of IEEE-754 binary representation of two half */
/*              floats. This value is primarily the difference of the    */
/*              mantissa bits, so to some extent, it can be seen as a    */
/*              kind of `relative` difference.                           */
/* Argument fa0: absolute epsilon - the maximum acceptable difference    */
/*               between two fp16 values.                                */
/* Two fp16 values are compared equal if their relative difference do    */
/* not exceed relative epsilon OR their absolute differnces do not       */
/* exceed absolute epsilon.                                              */
/*************************************************************************/
vv_check_eq_hf:
1:
	flw ft0, 0(a0)
	flw ft1, 0(a1)

        /* Compare pass if two FP values match exactly, including +-inf */
	feq.s t0, ft0, ft1
	bnez t0, 3f

        /* Calculate absolute diffence and compare with fa0 */
	fsub.s ft0, ft0, ft1
	fabs.s ft0, ft0
	flt.s t0, ft0, fa0
	bnez t0, 3f

        /* Load FP16 binary representation */
	lh t2, 0(a0)
	lh t3, 0(a1)

        /* Compare nan: all-one exp bits and non-zero mantissa bits */
	andi t0, t2, 0x3ff
	beqz t0, 2f
	andi t0, t3, 0x3ff
	beqz t0, 2f
	srli t0, t2, 10
	andi t0, t0, 0x1f
	li   t1, 0x1f
	bne  t0, t1, 2f
	srli t0, t3, 10
	andi t0, t0, 0x1f
	li   t1, 0x1f
	bne  t0, t1, 2f
	j    3f
2:
        /* Compare relative difference with a3 */
	srli t0, t2, 15
	srli t1, t3, 15
        /* Compare sign bits */
	bne t0, t1, 4f
        /* t0 = abs(t2 - t3) */
	sub t0, t2, t3
	srai t1, t0, 31
	add t0, t0, t1
	xor t0, t0, t1
	bgt t0, a3, 4f
3:
	addi a0, a0, 2
	addi a1, a1, 2
	addi a2, a2, -1
	bnez a2, 1b
	li a0, 0
	ret
4:
	li a0, 1
	ret

#define VV_CHECK_EQ_HF(vec1, vec2, vlen, abs_epsilon, rel_epsilon) \
    la a0, vec1;    \
    la a1, vec2;    \
    li a2, vlen;    \
    li a3, rel_epsilon; \
    la t0, 1f; \
    flw fa0, 0(t0); \
    call vv_check_eq_hf; \
    beqz a0, 2f; \
    j fail; \
2: \
    .pushsection .data; \
    .align 4; \
1: \
    .float abs_epsilon; \
    .popsection

#define VV_CHECK_EQ_HF_DEFAULT(vec1, vec2, vlen) \
    VV_CHECK_EQ_HF(vec1, vec2, vlen, VV_CHECK_EQ_HF_ATOL, VV_CHECK_EQ_HF_RTOL)

/* Compare accumulative difference of two FP16 vectors. Take the accumulation
   iterations into account because the error is accumulated during the iteration.
   acc: the number of accumulations before the result is calculated from inputs.
*/
#define VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, abs_epsilon, rel_epsilon, acc) \
    la a0, vec1;    \
    la a1, vec2;    \
    li a2, vlen;    \
    li a3, rel_epsilon; \
    la t0, 1f; \
    flw ft0, 0(t0); \
    flw ft2, 4(t0); \
    \
    /* abs_epsilon = (abs_epsilon * acc) */ \
    li t0, acc; \
    fcvt.s.w ft1, t0; \
    fmul.s fa0, ft1, ft0; \
    \
    /* rel_epsilon = (rel_epsilon * sqrt(2*acc)) */ \
    fmul.s ft1, ft1, ft2; \
    fsqrt.s ft1, ft1; \
    fcvt.s.w ft0, a3; \
    fmul.s ft0, ft0, ft1; \
    fcvt.w.s a3, ft0; \
    call vv_check_eq_hf; \
    beqz a0, 2f; \
    j fail; \
2: \
    .pushsection .data; \
    .align 4; \
1: \
    .float abs_epsilon; \
    .float 2.0; \
    .popsection

#define VV_CHECK_EQ_INT(vec1, vec2, vlen, ldins, esize) \
    la t0, vec1;    \
    la t1, vec2;    \
    li t2, vlen;    \
1: \
    ldins t3, 0(t0); \
    ldins t4, 0(t1); \
    beq t3, t4, 2f; \
    j fail; \
2: \
    addi t0, t0, esize; \
    addi t1, t1, esize; \
    addi t2, t2, -1; \
    bnez t2, 1b;

#define VV_CHECK_EQ_INT64(vec1, vec2, vlen) VV_CHECK_EQ_INT(vec1, vec2, vlen, ld, 8)
#define VV_CHECK_EQ_INT32(vec1, vec2, vlen) VV_CHECK_EQ_INT(vec1, vec2, vlen, lw, 4)
#define VV_CHECK_EQ_INT16(vec1, vec2, vlen) VV_CHECK_EQ_INT(vec1, vec2, vlen, lh, 2)
#define VV_CHECK_EQ_INT8(vec1, vec2, vlen) VV_CHECK_EQ_INT(vec1, vec2, vlen, lb, 1)


#define VV_CHECK_EQ_INT_CLOSE(vec1, vec2, vlen, ldins, esize, epsilon) \
    la t0, vec1;    \
    la t1, vec2;    \
    li t2, vlen;    \
1: \
    ldins t3, 0(t0); \
    ldins t4, 0(t1); \
    \
    srli t5, t3, 7; \
    srli t6, t4, 7; \
    beq t5, t6, 2f; \
    j fail; \
2: \
    /* t0 = abs(t2 - t3) */ \
    sub t5, t3, t4; \
    srai t6, t5, 31; \
    add t5, t5, t6; \
    xor t5, t5, t6; \
    li a3, epsilon; \
    ble t5, a3, 3f; \
    j fail; \
3: \
    addi t0, t0, esize; \
    addi t1, t1, esize; \
    addi t2, t2, -1; \
    bnez t2, 1b;

#define VV_CHECK_EQ_INT32_CLOSE(vec1, vec2, vlen, epsilon) \
    VV_CHECK_EQ_INT_CLOSE(vec1, vec2, vlen, lw, 4, epsilon)
#define VV_CHECK_EQ_INT16_CLOSE(vec1, vec2, vlen, epsilon) \
    VV_CHECK_EQ_INT_CLOSE(vec1, vec2, vlen, lh, 2, epsilon)
#define VV_CHECK_EQ_INT8_CLOSE(vec1, vec2, vlen, epsilon) \
    VV_CHECK_EQ_INT_CLOSE(vec1, vec2, vlen, lb, 1, epsilon)



#endif
