# RISC-V Testsuite

## 开发说明

在vscode中搜索并安装 Python Test Explorer for Visual Studio Code 插件

![Python Test Explorer](docs/images/python-test-explorer.png)

然后就可以在vscode里进行test case的开发了。

![Python Test Working](docs/images/python-test-working.png)

开发前需求安装python依赖，推荐使用virtualenv的方式。

    $ virtualenv -p python3 .env
    $ source .env/bin/activate
    $ pip install -r requirements.txt

## TODO:

* 丰富cases，包含 rvv，custom，及rvgc指令。
* 优化simulate函数，允许多个case合并后执行
* 定制指令操作数在python中比对
* 添加torture随机验证功能
* 添加palladium，haps，其它仿真器比对功能
* 添加更多的调试信息
* 添加代码检查工具

