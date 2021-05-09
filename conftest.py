option = None

def pytest_addoption(parser):
    parser.addoption('--specs', help='test specs')
    parser.addoption('--cases', help='test cases, for example:\nTest_addi::test_imm_op[0-0]')

    parser.addoption('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
    parser.addoption('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
    parser.addoption('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
    parser.addoption('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
    parser.addoption('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

    parser.addoption('--clang', help='path of clang compiler', default='clang')

    parser.addoption('--spike', help='path of spike simulator', default='spike')
    parser.addoption('--vcs', help='path of vcs simulator', default=None)
    parser.addoption('--verilator', help='path of verilator simulator', default=None)
