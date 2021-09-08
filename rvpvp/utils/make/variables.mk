rootdir := ../../../..

CC = clang --target=riscv64-unknown-elf -mno-relax -fuse-ld=lld -march=rv64gv0p10zfh0p1 -menable-experimental-extensions
CFLAGS = -DXLEN=64 -DVLEN=1024 -g -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles -I$(rootdir)/env/p -I$(rootdir)/macros/scalar -I$(rootdir)/macros/vector -I$(rootdir)/macros/stc
LDFLAGS = -T$(rootdir)/env/p/link.ld  -Wl,-Map,test.map

OBJDUMP = riscv64-unknown-elf-objdump -S -D

SPIKE = spike
SPIKE_OPTS = --isa=rv64gcv_zfh --varch=vlen:1024,elen:64,slen:1024 +signature-granularity=32

GEM5_PATH = ~/work/gem5/gem5
GEM5 = $(GEM5_PATH)/build/RISCV/gem5.opt
GEM5_OPTS = \
	--debug-flags=Exec --listener-mode=off \
	$(GEM5_PATH)/configs/example/fs.py \
	--cpu-type=MinorCPU \
	--bp-type=LTAGE \
	--num-cpu=1 \
	--mem-channels=1 \
	--mem-size=3072MB \
	--caches \
	--l1d_size=32kB \
	--l1i_size=32kB \
	--cacheline_size=64 \
	--l1i_assoc=8 \
	--l1d_assoc=8 \
	--l2cache \
	--l2_size=512kB \
