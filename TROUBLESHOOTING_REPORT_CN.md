# 故障排除报告：Gen2 RFID Reader 启动脚本修复

**日期：** 2026年1月9日
**作者：** Gemini CLI Agent

## 1. 问题概述
在尝试运行 `run_reader.sh` 启动脚本时，遇到了一系列阻碍程序正常启动的问题。主要表现为权限错误、Python 模块缺失报错 (`ModuleNotFoundError`) 以及段错误 (`Segmentation Fault`)。

## 2. 详细解决步骤与思考过程

### 步骤一：解决执行权限问题
*   **现象：** 首次运行 `./run_reader.sh` 时，系统提示 `Permission denied`（权限不够）。
*   **思考：** Linux 下脚本文件必须具有可执行权限才能直接运行。
*   **操作：** 尝试使用 `chmod +x` 添加权限，但最终通过 `sudo bash run_reader.sh` 绕过权限位检查并以超级用户权限执行，这对于后续操作硬件（USRP）也是必要的。

### 步骤二：修复 Python 模块导入错误 (`ModuleNotFoundError: No module named 'rfid'`)
*   **现象：** 脚本执行后，Python 抛出无法找到 `rfid` 模块的错误。
*   **思考：** `PYTHONPATH` 环境变量没有正确指向编译生成的 Python 绑定文件。原始脚本指向了 `test_modules/gnuradio`，但实际构建产物结构可能不同。
*   **排查：**
    1.  检查 `gr-rfid/build/test_modules`，发现为空。
    2.  检查 `gr-rfid/build/python`，发现存在 `rfid` 目录，但缺少标准的 Python 包结构文件（如 `__init__.py`）。
    3.  检查源码目录 `gr-rfid/python/rfid/__init__.py`，确认其包含了导入绑定的逻辑。
*   **操作：**
    1.  手动将源码中的 `__init__.py` 复制到构建目录 `gr-rfid/build/python/rfid/`。
    2.  在构建目录中创建指向共享库 (`.so`) 的软链接，确保 `__init__.py` 能正确加载 C++ 扩展。
    3.  修改 `run_reader.sh`，将 `PYTHONPATH` 更新为 `$SCRIPT_DIR/gr-rfid/build/python`。

### 步骤三：解决段错误 (`Segmentation Fault`) 与 动态库加载
*   **现象：** 解决了模块导入后，程序在初始化阶段崩溃，报段错误。
*   **思考：**
    1.  段错误通常意味着 C++ 层面的内存访问违规或动态库版本不匹配/找不到。
    2.  GNU Radio 的 OOT (Out-of-Tree) 模块依赖于生成的 C++ 共享库 (`libgnuradio-rfid.so`)。
    3.  虽然脚本中设置了 `LD_LIBRARY_PATH`，但在使用 `sudo` 时，处于安全考虑，环境变量往往会被重置或不被传递。
*   **操作：**
    1.  修改 `run_reader.sh` 中的 `sudo` 命令，显式传递 `LD_LIBRARY_PATH` 和 `PYTHONPATH`。
    2.  添加 `python3 -u` 参数以禁用输出缓冲，以便更早看到崩溃前的日志。

### 步骤四：修正工作目录路径问题
*   **现象：** 程序依然崩溃。
*   **思考：** 程序内部（`reader.py`）使用了相对路径来访问资源或写入日志（例如 `../misc/data/...`）。如果直接从根目录运行脚本，这些相对路径解析会出错，可能导致文件操作失败进而引发崩溃（尤其是在 C++ 层面没有做好空指针检查时）。
*   **操作：** 修改 `run_reader.sh`，在执行 Python 脚本前先 `cd` 到 `gr-rfid/apps` 目录，确保运行时环境与开发/测试时的假设一致。

## 3. 最终结果
经过上述修正，脚本现在可以正确设置环境、加载模块并启动 RFID Reader 主程序。

## 4. 后续建议 (What's Next)
1.  **验证硬件连接：** 确保 USRP 设备已连接且 IP 地址配置正确（默认 192.168.40.2）。如果设备未连接，程序可能会在初始化 USRP Source/Sink 时报错。
2.  **日志监控：** 如果程序运行中遇到逻辑问题，建议检查 `misc/data/` 下的数据转储文件。
3.  **构建系统优化：** 建议检查 `CMake` 配置，确保安装（`make install`）过程能自动正确部署 Python 文件，避免手动复制 `__init__.py` 这种临时修复方式。
4.  **权限管理：** 考虑配置 `udev` 规则允许非 root 用户访问 USRP 设备，以减少使用 `sudo` 带来的环境变量传递麻烦和安全风险。
