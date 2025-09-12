import pandas as pd
import numpy as np

# 读取4fix.xlsx文件
fix_filepath = '/home/tianfang/project_Mat_new/4fix.xlsx'
fix_data = pd.read_excel(fix_filepath, sheet_name='4fix')

# 读取4simply.xlsx文件
simply_filepath = '/home/tianfang/project_Mat_new/4simply.xlsx'
simply_data = pd.read_excel(simply_filepath, sheet_name='4simply')

# 提取所需列并转换为numpy数组
fix_coordinates = fix_data[['X Location (m)', 'Y Location (m)', 'Total Deformation (m)']].to_numpy()
simply_coordinates = simply_data[['X Location (m)', 'Y Location (m)', 'Total Deformation (m)']].to_numpy()

# 保存为numpy格式
fix_save_path = '/home/tianfang/project_Mat_new/fix_coordinates.npy'
simply_save_path = '/home/tianfang/project_Mat_new/simply_coordinates.npy'

np.save(fix_save_path, fix_coordinates)
np.save(simply_save_path, simply_coordinates)

# 输出数据检查
print(f"4fix坐标数据已保存至: {fix_save_path}")
print(f"4simply坐标数据已保存至: {simply_save_path}")

