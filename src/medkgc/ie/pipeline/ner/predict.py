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
from medkgc.ie.pipeline.re.re import extract_relations, load_shots, format_shots

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

def main(args):
    '''predict the radgraph dataset using the llm, then save the result
    
    Args:
        args: 解析后的命令行参数
    '''

    # 输出现在开始预测
    print(f'现在开始预测，使用{args.num_shots}个shots')

    # 加载测试数据
    try:
        with open(args.data_path, 'r') as f:
            data: Dict[str, Any] = json.load(f)
    except FileNotFoundError:
        print(f'错误: 找不到数据文件 {args.data_path}')
        sys.exit(1)

    json_result_list = []
    
    # 创建输出目录
    output_dir = os.path.join('src/medkgc/ie/pipeline/ner/results')
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, f'ner_pred_{args.num_shots}.json')

    # 如果文件存在，加载已有结果并从最后一个继续
    start_index = args.start_index
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                json_result_list = json.load(f)
            # 更新起始索引为已处理的最后一个样本的索引+1
            start_index = len(json_result_list)
            print(f'已加载{len(json_result_list)}个已处理的结果，从索引{start_index}继续处理')
        except FileNotFoundError:
            print(f'警告: 未找到已有的结果文件，将从头开始处理')
    else:
        print(f'未找到结果文件，将从头开始处理')

    # 加载few-shot示例
    shots = load_shots('data/radgraph/original/train.json', num_shots=args.num_shots)
    formatted_shots = format_shots(shots)

    # 遍历每个样本进行评估
    for index, (key, value) in enumerate(data.items()):
        if index < start_index:
            continue
            
        text = value['text']
        
        try:
            # 使用重试机制处理样本
            entities = process_sample(text, args.num_shots)
            pred = ner_eval.entities_from_llm_response(entities, text)
            
            # 进行关系抽取
            relations = extract_relations(text, entities, model=None, shots=formatted_shots)
            
            # 保存结果
            json_result_list.append({'text': text, 'pred': pred, 'relations': relations})
            
            # 每处理一个样本就保存一次结果
            with open(file_path, 'w') as f:
                json.dump(json_result_list, f)
                
            print(f'已处理 {index + 1}/{len(data)} 个样本')
            
        except Exception as e:
            print(f'错误: 样本 {index} 处理失败')
            print(f'错误信息: {str(e)}')
            print(text)
            print(f'请使用 --start_index {index} 从该样本重新开始处理')
            sys.exit(1)
    
    # 输出预测完成
    print(f'预测完成，结果已保存到 {file_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run NER prediction with specified parameters')
    parser.add_argument('--num_shots', type=int, default=100,
                      help='Number of few-shot examples to use (default: 100)')
    parser.add_argument('--start_index', type=int, default=0,
                      help='Start processing from this index (default: 0)')
    parser.add_argument('--data_path', type=str, default='data/radgraph/splits/dev_mimic.json',
                      help='Path to the input data file (default: data/radgraph/splits/dev_mimic.json)')
    
    args = parser.parse_args()
    
    main(args)

    print(f"\n预测完成，开始评估结果...")
    from medkgc.ie.pipeline.ner.eval_ner import main as eval_main
    eval_main(num_shots=args.num_shots)
