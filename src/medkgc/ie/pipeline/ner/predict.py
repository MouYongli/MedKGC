"""
NER预测脚本

这个脚本使用大语言模型(LLM)对RadGraph数据集进行命名实体识别(NER)预测。主要功能包括：

1. 数据处理：
   - 读取开发集数据(dev.json or test.json)
   - 每个样本的原始文本在key为'text'的字段中
   
2. 实体预测：
   - 使用LLM对每个报告进行实体抽取
   - 支持few-shot学习，默认使用50个示例
   - 预测结果包含实体类型和位置信息
   
3. 结果保存：
   - 将预测结果保存为JSON格式，内容是json list。
   - 每个样本的结果包含原始文本和预测的实体列表
   - 实时保存结果，避免中断导致数据丢失

使用方法：
    python -m src.medkgc.ie.pipeline.ner.predict --num_shots 100 --start_index 0

输出文件：
    src/medkgc/ie/pipeline/ner/outputs/ner_pred.json
"""

import json
import sys
import argparse
import time
import os
from typing import Dict, Any

from medkgc.ie.pipeline.ner.utils import ner_eval
from medkgc.ie.pipeline.ner.utils.entity_extractor import extract_entities

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
                time.sleep(1)  # 添加短暂延迟，避免立即重试
                continue

def load_data(data_path: str) -> Dict[str, Any]:
    """加载测试数据"""
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'错误: 找不到数据文件 {data_path}')
        sys.exit(1)

def save_results(file_path: str, results: dict):
    """保存预测结果"""
    with open(file_path, 'w') as f:
        json.dump(results, f)

def create_output_dir(output_dir: str):
    """创建输出目录"""
    os.makedirs(output_dir, exist_ok=True)

def load_existing_results(file_path: str) -> dict:
    """加载已有的结果文件"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'警告: 未找到已有的结果文件，将从头开始处理')
    return {}

def process_samples(data: Dict[str, Any], num_shots: int, file_path: str):
    """处理所有样本"""
    json_result_dict = load_existing_results(file_path)

    for key, value in data.items():
        if key in json_result_dict:
            continue

        text = value['text']
        try:
            entities = process_sample(text, num_shots)
            
            json_result_dict[key] = ner_eval.entities_from_llm_response(entities, text)

            save_results(file_path, json_result_dict)

            print(f'已处理 {len(json_result_dict)}/{len(data)} 个样本')
        except Exception as e:
            print(f'错误: 样本 {key} 处理失败')
            print(f'错误信息: {str(e)}')
            print(text)
            print(f'请重新开始处理')
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run NER prediction with specified parameters')
    parser.add_argument('--num_shots', type=int, default=100,
                        help='Number of few-shot examples to use (default: 100)')
    parser.add_argument('--data_path', type=str, default='data/radgraph/splits/dev_mimic.json',
                        help='Path to the input data file (default: data/radgraph/splits/dev_mimic.json)')

    
    args = parser.parse_args()

    print(f'现在开始预测，使用{args.num_shots}个shots')

    data = load_data(args.data_path)

    output_dir = os.path.join('src/medkgc/ie/pipeline/ner/results')
    create_output_dir(output_dir)
    file_path = os.path.join(output_dir, f'ner_pred_{args.num_shots}.json')

    process_samples(data, args.num_shots, file_path)

    print(f'预测完成，结果已保存到 {file_path}')
    print(f"\n预测完成，开始评估结果...")