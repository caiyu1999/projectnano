

from optparse import Option
import pandas as pd
import numpy as np
import json
import os
import sys
from dataclasses import dataclass 
from typing import List, Dict, Any, Optional,Union, Tuple
from pathlib import Path





@dataclass 
class ColumnInfo:
    """列信息"""
    name: str
    dtype: str
    null_count: int
    unique_count: int
    sample_values: List[Any]  # 前几个非空值作为示例

@dataclass
class SheetInfo:
    """工作表信息"""
    name: str
    rows: int
    columns: int
    columns_info: List[ColumnInfo]
    sample_data: List[Dict[str, Any]]  # 前几行数据
    statistical_summary: Optional[Dict[str, Any]]  # 数值列的统计摘要

@dataclass
class StructureExcel:
    """Excel文件结构信息"""
    file_type = "excel"
    file_path: str
    total_sheets: int
    sheets_info: List[SheetInfo]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，方便序列化"""
        return {
            'file_type': self.file_type,
            'file_path': self.file_path,
            'total_sheets': self.total_sheets,
            'sheets_info': [
                {
                    'name': sheet.name,
                    'rows': sheet.rows,
                    'columns': sheet.columns,
                    'columns_info': [
                        {
                            'name': col.name,
                            'dtype': col.dtype,
                            'null_count': col.null_count,
                            'unique_count': col.unique_count,
                            'sample_values': col.sample_values
                        } for col in sheet.columns_info
                    ],
                    'sample_data': sheet.sample_data,
                    'statistical_summary': sheet.statistical_summary
                } for sheet in self.sheets_info
            ]
        }
    
    def to_json_string(self) -> str:
        """转换为JSON字符串格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def get_summary_text(self) -> str:
        """获取结构摘要文本，适合直接发送给大模型"""
        def format_value(val):
            # 如果是float类型，保留3位小数
            if isinstance(val, float):
                return f"{val:.3f}"
            # 如果是list，递归处理
            if isinstance(val, list):
                return [format_value(v) for v in val]
            # 如果是dict，递归处理
            if isinstance(val, dict):
                return {k: format_value(v) for k, v in val.items()}
            return val

        summary = f"{self.file_type}文件: {self.file_path}\n"
        summary += f"工作表总数: {self.total_sheets}\n\n"
        
        for sheet in self.sheets_info:
            summary += f"工作表: {sheet.name}\n"
            summary += f"  尺寸: {sheet.rows}行 x {sheet.columns}列\n"
            summary += f"  列信息:\n"
            
            for col in sheet.columns_info:
                summary += f"    - {col.name}: {col.dtype} (缺失值: {col.null_count}, 唯一值: {col.unique_count})\n"
                if col.sample_values:
                    # 对示例值做格式化
                    formatted_samples = [format_value(v) for v in col.sample_values[:3]]
                    summary += f"      示例值: {formatted_samples}\n"
            
            summary += f"  前3行数据:\n"
            for i, row in enumerate(sheet.sample_data[:3]):
                # 对每一行的值做格式化
                formatted_row = {k: format_value(v) for k, v in row.items()}
                summary += f"    第{i+1}行: {formatted_row}\n"
            
            summary += "\n"
        
        return summary



def comprehensive_excel_analysis(file_path: str,code = None) -> Optional[Union[ str, StructureExcel, Tuple[str, str]]]:
    """
    全面分析Excel文件并返回StructureExcel对象
    这个文件可能有密码 我们暂时不考虑这种情况 后期再添加
    """
    
    try:
       
        try:
            all_sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        except Exception as e:
            return str(e)
        
        
        sheets_info = []
        
        for sheet_name, df in all_sheets.items():
            try:
                # 检查工作表是否为空
                if df.empty:
                    return f"工作表 '{sheet_name}' 为空"
                
                # 检查工作表大小
                if df.shape[0] > 1000000 or df.shape[1] > 10000:  # 100万行或1万列
                    return f"工作表 '{sheet_name}' 过大: {df.shape[0]}行 x {df.shape[1]}列"
                
                # 创建列信息列表
                columns_info = []
                for col_name in df.columns:
                    try:
                        col_data = df[col_name]
                        # 获取非空值的示例
                        sample_values = col_data.dropna().head(3).tolist()
                        
                        column_info = ColumnInfo(
                            name=str(col_name),
                            dtype=str(col_data.dtype),
                            null_count=int(col_data.isnull().sum()),
                            unique_count=int(col_data.nunique()),
                            sample_values=sample_values
                        )
                        columns_info.append(column_info)
                    except Exception as e:
                        return  f"解析列 '{col_name}' 时出错: {str(e)}"
            
                # # 获取统计摘要
                # try:
                #     numeric_cols = df.select_dtypes(include=[np.number]).columns
                #     statistical_summary = None #df.describe().to_dict() if len(numeric_cols) > 0 else None
                # except Exception as e:
                #     statistical_summary = None  # 如果统计摘要失败，设为None
                
                # 创建工作表信息
                sheet_info = SheetInfo(
                    name=str(sheet_name),
                    rows=df.shape[0],
                    columns=df.shape[1],
                    columns_info=columns_info,
                    sample_data=df.head(3).to_dict('records'),
                    statistical_summary=None
                )
                sheets_info.append(sheet_info)
                
            except Exception as e:
                return f"处理工作表 '{sheet_name}' 时出错: {str(e)}"
        
        # 创建StructureExcel对象
        structure = StructureExcel(
            file_path=file_path,
            total_sheets=len(all_sheets),
            sheets_info=sheets_info
        )
        
        return structure
        
    except Exception as e:
        return f"未知错误: {str(e)}"

