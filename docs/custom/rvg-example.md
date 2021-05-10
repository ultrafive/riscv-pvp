# RISC-V G Example

```yaml
_: &default
  env: RVTEST_RV32U
  templates:
    test_imm_op @ rs1, imm: |
      TEST_IMM_OP( {num}, {name}, {res}, {rs1}, {imm} );
    test_src1_eq_dest @ rs1, imm: |
      TEST_IMM_SRC1_EQ_DEST( {num}, {name}, {res}, {rs1}, {imm} );
    test_dest_bypass @ rs1, imm, nop_cycles: |
      TEST_IMM_DEST_BYPASS( {num}, {nop_cycles}, {name}, {res}, {rs1}, {imm} );
    test_src1_bypass @ rs1, imm, nop_cycles: |
      TEST_IMM_SRC1_BYPASS( {num}, {nop_cycles}, {name}, {res}, {rs1}, {imm} );
    test_zerosrc1 @ imm @ rs1 = 0: |
      TEST_IMM_ZEROSRC1( {num}, {name}, {res}, {imm} );
    test_zerodest @ rs1, imm: |
      TEST_IMM_ZERODEST( {num}, {name}, {rs1}, {imm} );

addi:
  <<: *default
  cases:
    test_imm_op:
      - [ 0x00000000, 0x000 ]
      - [ 0x00000001, 0x001 ]
      - [ 0x00000003, 0x007 ]

      - [ 0x0000000000000000, 0x800 ]
      - [ 0xffffffff80000000, 0x000 ]
      - [ 0xffffffff80000000, 0x800 ]

      - [ 0x00000000, 0x7ff ]
      - [ 0x7fffffff, 0x000 ]
      - [ 0x7fffffff, 0x7ff ]

      - [ 0xffffffff80000000, 0x7ff ]
      - [ 0x000000007fffffff, 0x800 ]

      - [ 0x0000000000000000, 0xfff ]
      - [ 0xffffffffffffffff, 0x001 ]
      - [ 0xffffffffffffffff, 0xfff ]

      - [ 0x7fffffff, 0x001 ]

    test_src1_eq_dest:
      - [ 13, 11 ]
    
    test_dest_bypass:
      - [ 13, 11, 0 ]
      - [ 13, 10, 1 ]
      - [ 13,  9, 2 ]

    test_src1_bypass:
      - [ 13, 11, 0 ]
      - [ 13, 10, 1 ]
      - [ 13,  9, 2 ]

    test_zerosrc1:
      - [ 32 ]
      
    test_zerodest:
      - [ 33, 50 ]

slti:
  <<: *default
  cases:
    test_imm_op:
      - [ 0x0000000000000000, 0x000 ]
      - [ 0x0000000000000001, 0x001 ]
      - [ 0x0000000000000003, 0x007 ]
      - [ 0x0000000000000007, 0x003 ]

      - [ 0x0000000000000000, 0x800 ]
      - [ 0xffffffff80000000, 0x000 ]
      - [ 0xffffffff80000000, 0x800 ]

      - [ 0x0000000000000000, 0x7ff ]
      - [ 0x000000007fffffff, 0x000 ]
      - [ 0x000000007fffffff, 0x7ff ]

      - [ 0xffffffff80000000, 0x7ff ]
      - [ 0x000000007fffffff, 0x800 ]

      - [ 0x0000000000000000, 0xfff ]
      - [ 0xffffffffffffffff, 0x001 ]
      - [ 0xffffffffffffffff, 0xfff ]

    test_src1_eq_dest:
      - [ 11, 13 ]
```