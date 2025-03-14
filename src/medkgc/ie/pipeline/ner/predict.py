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
from typing import Dict, Any, List, Tuple

from medkgc.ie.pipeline.ner.utils.entity_extractor import (
    extract_entities_with_llm, 
    convert_tuples_to_json,
    extract_entities_with_llm_with_retry
)
from medkgc.ie.pipeline.ner.utils.data_loader import load_json_data

def load_prediction_results(json_path: str) -> Dict[str, List[Tuple[str, int, int]]]:
    """加载已有的预测结果文件
    
    Args:
        json_path: JSON文件路径
        
    Returns:
        Dict[str, List[Tuple[str, int, int]]]: 预测结果字典
    """
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'警告: 未找到已有的结果文件，将从头开始处理')
    return {}

def extract_entities_from_reports(data_dict: Dict[str, Any], num_shots: int, output_path: str, model_name: str):
    """批量处理文本并抽取实体
    
    Args:
        data_dict: 输入数据字典
        num_shots: few-shot示例数量
        output_path: 输出文件路径
        model_name: 使用的模型名称
    """

    # 加载已有的预测结果，如果存在则跳过，避免重复预测
    result_dict = load_prediction_results(output_path)

    for report_id, report_data in data_dict.items():
        if report_id in result_dict:
            continue

        report_text = report_data['text']
        
        try:
            # 处理单个样本
            entity_tuples = extract_entities_with_llm_with_retry(report_text, num_shots, model_name)

            result_dict[report_id] = convert_tuples_to_json(entity_tuples, report_text)

            # 保存结果
            with open(output_path, 'w') as f:
                json.dump(result_dict, f)

            print(f'已处理 {len(result_dict)}/{len(data_dict)} 个样本')
        except Exception as error:
            print(f'错误: 样本 {report_id} 处理失败')
            print(f'错误信息: {str(error)}')
            print(report_text)
            print(f'请重新开始处理')
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Run NER prediction with specified parameters')

    parser.add_argument('--num_shots', type=int, default=100,
                        help='Number of few-shot examples to use (default: 100)')
    parser.add_argument('--data_path', type=str, default='data/radgraph/splits/dev_mimic.json',
                        help='Path to the input data file (default: data/radgraph/splits/dev_mimic.json)')
    parser.add_argument('--output_dir', type=str, default='src/medkgc/ie/pipeline/ner/results',
                        help='Directory to save the output results (default: src/medkgc/ie/pipeline/ner/results)')
    parser.add_argument('--model_name', type=str, required=True,
                        help='Name of the model used for prediction')
    
    args = parser.parse_args()

    print(f'现在开始预测，使用{args.num_shots}个shots')

    # 加载数据
    data_dict = load_json_data(args.data_path)

    # 确保输出目录存在，如不存在则创建
    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, f'ner_pred_{args.model_name}_{args.num_shots}.json')

    # 处理样本
    extract_entities_from_reports(data_dict, args.num_shots, output_path, args.model_name)

    print(f'预测完成，结果已保存到 {output_path}')
    print(f"\n预测完成，开始评估结果...")

if __name__ == '__main__':
    main()