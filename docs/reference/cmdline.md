# Command Line Reference

```bash
./run.py --help
usage: run.py [-h] [--specs SPECS] [--cases CASES] [--xlen {32,64}]
              [--flen {32,64}] [--vlen {256,512,1024,2048}] [--elen {32,64}]
              [--slen {256,512,1024,2048}] [--clang CLANG] [--spike SPIKE]
              [--vcs VCS] [--verilator VERILATOR]

optional arguments:
  -h, --help            show this help message and exit
  --specs SPECS         test specs
  --cases CASES         test cases, for example: Test_addi::test_imm_op[0-0]

  --xlen {32,64}        bits of int register (xreg)
  --flen {32,64}        bits of float register (freg)
  --vlen {256,512,1024,2048}
                        bits of vector register (vreg)
  --elen {32,64}        bits of maximum size of vector element
  --slen {256,512,1024,2048}
                        bits of vector striping distance

  --clang CLANG         path of clang compiler

  --spike SPIKE         path of spike simulator
  --vcs VCS             path of vcs simulator
  --verilator VERILATOR
                        path of verilator simulator

```