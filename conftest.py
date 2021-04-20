option = None

def pytest_addoption(parser):
    parser.addoption("--specs", action="store", help="riscv-testsuite spec file")
