"""
NER预测脚本

这个脚本使用大语言模型(LLM)对RadGraph数据集进行命名实体识别(NER)预测。主要功能包括：

1. 数据处理：
   - 读取开发集数据(dev.json)，包含75个放射学报告样本
   - 每个样本包含原始文本和人工标注的实体
   
2. 实体预测：
   - 使用LLM对每个报告进行实体抽取
   - 支持few-shot学习，默认使用50个示例
   - 预测结果包含实体类型和位置信息
   
3. 结果保存：
   - 将预测结果保存为JSON格式
   - 每个样本的结果包含原始文本和预测的实体列表
   - 实时保存结果，避免中断导致数据丢失

预测的实体类型包括：
- OBS-DP: 确定存在的观察
- ANAT-DP: 确定存在的解剖结构
- OBS-U: 不确定的观察
- OBS-DA: 确定不存在的观察

使用方法：
    python ie/ner.py

输出文件：
    ie/outputs/ner_pred.json
"""

import json
import sys
import argparse
import time
from typing import Dict, Any

import utils.ner_eval as ner_eval
from utils.ner import extract_entities

def process_sample(text: str, num_shots: int) -> list:
    """处理单个样本，包含重试机制"""
    max_retries = 3

    for attempt in range(max_retries):
        try:
            entities = extract_entities(text, num_shots)
            return entities
        except Exception as e:
            if attempt < max_retries - 1:
                print(f'第{attempt + 1}次尝试失败: {e}')
                continue
            else:
                raise e

def main(start_index: int = 0, num_shots: int = 200):
    '''predict the radgraph dataset using the llm, then save the result
    
    Args:
        start_index: 从第几个样本开始处理（从0开始计数）
        num_shots: few-shot示例的数量
    '''
    
    # 加载测试数据
    with open('/home/hbchen/Projects/MedKGC/resource/radgraph/dev.json', 'r') as f:
        data: Dict[str, Any] = json.load(f)

    json_result_list = []
    file_path = f'ie/outputs/ner_pred_{num_shots}.json'

    # 如果start_index > 0，则先加载已有的结果
    if start_index > 0:
        try:
            with open(file_path, 'r') as f:
                json_result_list = json.load(f)
            print(f'已加载{len(json_result_list)}个已处理的结果')
        except FileNotFoundError:
            print(f'警告: 未找到已有的结果文件，将从头开始处理')

    # 遍历每个样本进行评估
    for index, (key, value) in enumerate(data.items()):
        if index < start_index:
            continue
            
        text = value['text']
        
        try:
            # 使用重试机制处理样本
            entities = process_sample(text, num_shots)
            pred = ner_eval.entities_from_llm_response(entities, text)
            
            # 保存结果
            json_result_list.append({'text': text, 'pred': pred})
            
            # 每处理一个样本就保存一次结果
            with open(file_path, 'w') as f:
                json.dump(json_result_list, f)
                
            print(f'已处理 {index + 1}/{len(data)} 个样本')
            
        except Exception as e:
            print(f'错误: 样本 {index} 处理失败')
            print(f'错误信息: {str(e)}')
            print(f'请使用 main({index}, num_shots={num_shots}) 从该样本重新开始处理')
            sys.exit(1)

if __name__ == '__main__':
    main(num_shots=200)  # 从第51个样本开始处理，使用200个few-shot示例