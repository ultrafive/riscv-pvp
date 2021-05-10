# Getting Started

## Prerequisites

```bash
export RISCV=~/opt/riscv
```

### Toolchains

For latest rvv-0.10/1.0 support, we use llvm as the default toolchain.
We could build it from source and install to $RISCV. 

```bash
$ git clone https://github.com/ultrafive/llvm-project
$ cd llvm-project
$ git checkout uf-master
$ mkdir -p build && cd build && cmake -DCMAKE_INSTALL_PREFIX=$RISCV \
    -DCMAKE_BUILD_TYPE=Release -DLLVM_OPTIMIZED_TABLEGEN=On \
    -DLLVM_ENABLE_PROJECTS="clang;compiler-rt;lld" \
    -DLLVM_LINK_LLVM_DYLIB=On ../llvm
$ make -j`nproc` && make install
```

llvm's libc development is still in the planning phase. To support c compiling,
we still need a external libc. 
Let‘s build riscv-gnu-toolchain from source and install to $RISCV.

```bash
$ git clone https://github.com/riscv/riscv-gnu-toolchain
$ cd riscv-gnu-toolchain
$ git checkout rvv-0.9.x
$ git submodule update --init --recursive
$ mkdir -p build && cd build && ../configure --prefix=$RISCV
$ make -j`nproc`
```

### Instruction Set Simulators

The default Instruction Set Simulator (ISS) is spike. We are working in progress
to support more ISSs.

```base

$ git clone https://github.com/riscv/riscv-tools
$ cd riscv-tools
$ git submodule update --init --recursive
$ cd riscv-isa-sim && git checkout master && git pull && cd ..
$ ./build-spike-only.sh
```

### RTL Simulators

To use the co-simulation flow, you need to have an RTL simulator which supports
RISC-V Vector Extension 0.10/1.0. The RTL simulator also need to use
"+signature=" argument provide a way to dump the "begin_signature" section to
a file, this machanism is also used by riscv-torture or other RISC-V
co-simulation flows.

We have verified with Synopsys VCS, verilator in chipyard framework. Please make
sure the EDA tool environment is properly setup before running the co-simulation
flow.

## Install RISCV-PVP

Getting the source from github.

```bash
git clone https://github.com/ultrafive/riscv-pvp.git
```

Install dependencies and run.

```bash
cd riscv-pvp
pip3 install -r requirements.txt    # install dependencies (only once)
python3 run.py --help
```

Run verification with default spike ISS:

```bash
python3 ./run.py
```

Run verification with default spike ISS and diff with vcs RTL simulator:

```bash
python3 ./run.py --vcs=<simv_path>
```
