#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os

# 清除之前的图形
plt.close('all')

# 获取脚本所在目录，构建数据文件路径
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '../data/file_source_test')
file_path = os.path.normpath(file_path)

# 读取二进制文件
fi_1 = open(file_path, 'rb')

# 读取float32格式的数据
x_inter_1 = np.fromfile(fi_1, dtype=np.float32)
fi_1.close()

# 如果数据是复数格式（实部和虚部交替）
x_1 = x_inter_1[0::2] + 1j * x_inter_1[1::2]

# 绘制复数的绝对值
plt.plot(np.abs(x_1))
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Signal Amplitude')
plt.grid(True)
plt.show()
