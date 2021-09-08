#!/bin/bash
gem5_dir=$1
shift

$gem5_dir/build/RISCV/gem5.opt \
      --listener-mode=off \
      --debug-flags=Exec \
      $gem5_dir/configs/example/fs.py \
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
      $*
