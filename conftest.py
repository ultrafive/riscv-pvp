option = None

def pytest_addoption(parser):
    parser.addoption('--nproc', help='run tests on n processes', type=int, default=1)
    parser.addoption('--lsf', help='run tests on with lsf clusters', action="store_true")
    parser.addoption('--specs', help='test specs')
    parser.addoption('--cases', help='test case list string or file')
    parser.addoption('--basic-only', help='only run basic test cases for instructions', action="store_true")
    parser.addoption('--retry', help='retry last failed cases', action="store_true")

    parser.addoption('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
    parser.addoption('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
    parser.addoption('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
    parser.addoption('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
    parser.addoption('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

    parser.addoption('--clang', help='path of clang compiler', default='clang')

    parser.addoption('--spike', help='path of spike simulator', default='spike')
    parser.addoption('--vcs', help='path of vcs simulator', default=None)
    parser.addoption('--gem5', help='path of gem5 simulator', default=None)
    parser.addoption('--fsdb', help='generate fsdb waveform file when running vcs simulator', action="store_true")
    parser.addoption('--tsiloadmem', help='Load binary through TSI instead of backdoor', action="store_true")
    parser.addoption('--vcstimeout', help='Number of cycles after which VCS stops', default=1000000, type=int)
    parser.addoption('--verilator', help='path of verilator simulator', default=None)
