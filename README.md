# RISC-V Testsuite

基于pytest构建的模块化、参数化的RISC-V 指令集验证集。

## 功能

* 基础测试集以riscv-tests为模板生成
* 支持risc-v vector指令扩展
* 支持随机代码生成验证
* 支持多种仿真器及实际硬件平台的结果比对
* 通过numpy支持更丰富的数据的生成及功能验证
* 基于allure生成丰富的report，与JIRA集成

## TODO List:

* 丰富isa cases
   * rvgc *high*
   * rvv *high*
   * stc custom
* 定制指令操作数在python中比对 *high*
* 优化simulate函数，允许多个case合并后执行
* 添加torture随机验证功能
* 添加palladium，haps，其它仿真器比对功能
* 通过多种env完善case
   * p(physical)
   * pm(多线程)
   * pt(含中断)
   * v(virtual memory)

## RVV指令实现优先级

1. config, vset\*vl\*
2. load/store
3. int basic, fp basic
4. fma
5. misc

## 开发说明

    $ export RISCV=~/opt/riscv-next

### 安装 toolchain 和 simulator

    $ git clone https://github.com/riscv/riscv-gnu-toolchain
    $ cd riscv-gnu-toolchain
    $ mkdir -p build && cd build && ../configure --prefix=$RISCV
    $ make -j`nproc`

    $ git clone https://github.com/riscv/riscv-tools
    $ cd riscv-tools
    $ git submodule update --init --recursive
    $ ./build.sh

### 安装python依赖

开发前需求安装python依赖，推荐使用virtualenv的方式。

    $ cd riscv-testsuite
    $ virtualenv -p python3 .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt

### 安装vscode插件

在vscode中搜索并安装 Python Test Explorer for Visual Studio Code 插件

![Python Test Explorer](docs/images/python-test-explorer.png)

然后就可以在vscode里进行test case的开发了。

![Python Test Working](docs/images/python-test-working.png)
