import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 读取文件
fix_data = pd.read_excel('/home/tianfang/project_Mat_new/4fix.xlsx', sheet_name='4fix')
simply_data = pd.read_excel('/home/tianfang/project_Mat_new/4simply.xlsx', sheet_name='4simply')

# 提取所需的数据
fix_coords = fix_data[['X Location (m)', 'Y Location (m)', 'Total Deformation (m)']].values
simply_coords = simply_data[['X Location (m)', 'Y Location (m)', 'Total Deformation (m)']].values

# 使用numpy数组保存数据，命名规律为data_4fix和data_4simply
np.save('/home/tianfang/project_Mat_new/data_4fix.npy', fix_coords)
np.save('/home/tianfang/project_Mat_new/data_4simply.npy', simply_coords)

# 创建3D可视化
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制4fix数据点
ax.scatter(fix_coords[:, 0], fix_coords[:, 1], fix_coords[:, 2], c='r', label='4fix', alpha=0.6)

# 绘制4simply数据点
ax.scatter(simply_coords[:, 0], simply_coords[:, 1], simply_coords[:, 2], c='b', label='4simply', alpha=0.6)

# 设置标签和图例
ax.set_xlabel('X Location (m)')
ax.set_ylabel('Y Location (m)')
ax.set_zlabel('Total Deformation (m)')
ax.set_title('3D Visualization of 4fix and 4simply Data')
ax.legend()

# 保存图像
plt.savefig('/home/tianfang/project_Mat_new/3D_visualization.png')