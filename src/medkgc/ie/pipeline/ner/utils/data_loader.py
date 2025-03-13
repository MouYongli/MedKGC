"""
数据加载工具

提供用于加载和处理数据集的函数
"""

import json
from typing import Dict, Any

def load_json_data(file_path: str) -> Dict[str, Any]:
    """加载JSON格式的数据文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        Dict[str, Any]: 加载的数据字典
        
    Raises:
        FileNotFoundError: 如果文件不存在
        json.JSONDecodeError: 如果JSON格式不正确
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f'找不到文件: {file_path}')
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f'JSON格式错误: {str(e)}', e.doc, e.pos) 