// See LICENSE for license details.

#ifndef __TEST_MACROS_VEACC_M_DIM_H
#define __TEST_MACROS_VEACC_M_DIM_H

#include "test_macros.h"
#include "test_macros_stc.h"
#include "exception.h"

#define VV_CHECK_EQ(vec1, vec2, vlen, acc) VV_CHECK_EQ_HF_ACC(vec1, vec2, vlen, 0.05, 50, acc)

#include "vexxx_m_dim.h"

#endif
