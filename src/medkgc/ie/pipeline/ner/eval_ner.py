"""
NER评估脚本

这个脚本用于评估命名实体识别(NER)的预测结果。主要功能包括：

1. 读取数据：
   - 加载目标数据集(如dev.json)作为真实标注
   - 加载预测结果(如ner_pred.json)
   
2. 评估每个报告：
   - 将预测结果和真实标注转换为统一的Entity格式
   - 计算每个报告的精确率(Precision)和召回率(Recall)
   
3. 计算总体指标：
   - 正确预测数(Correct)
   - 错误预测数(Incorrect)
   - 未预测数(Missed)
   - 多余预测数(Spurious)
   - 总体精确率(Precision)
   - 总体召回率(Recall)
   - F1分数

使用方法：
    # 测试请指定prediction_path和target_path
    python -m src.medkgc.ie.pipeline.ner.eval_ner \
        --prediction_path src/medkgc/ie/pipeline/ner/results/test/ner_pred_llama_5.json \
        --target_path data/radgraph/splits/test_mimic.json \
        --output_dir src/medkgc/ie/pipeline/ner/results/test

输出文件：
    src/medkgc/ie/pipeline/ner/results/xxx/xxx.txt
"""

import json
import argparse
import os
from typing import Dict, Any, List, Tuple

from medkgc.ie.pipeline.ner.utils.data_loader import (
    load_json_data, 
    get_entities_from_data,
    extract_metadata_from_paths
)
from medkgc.ie.pipeline.ner.utils.data_formatter import (
    convert_pred_to_entities,
    format_total_metrics
)
from medkgc.ie.pipeline.ner.utils.ner_metrics import (
    Entity,
    compute_metrics,
    entities_from_radgraph
)

def aggregate_metrics(metrics_list: list, is_multi_labeler: bool = False) -> dict:
    """汇总评估指标"""
    if not is_multi_labeler:
        return aggregate_single_metrics(metrics_list)
    
    # 分别汇总与每个标注者的指标
    labeler_totals = []
    for labeler_idx in range(2):  # 假设有2个标注者
        labeler_metrics = [m[labeler_idx] for m in metrics_list if m]
        labeler_totals.append(aggregate_single_metrics(labeler_metrics))
    
    # 只计算F1的平均值
    avg_f1 = sum(t['f1'] for t in labeler_totals) / len(labeler_totals)
    
    return {
        'labeler_1': labeler_totals[0],
        'labeler_2': labeler_totals[1],
        'avg_f1': avg_f1
    }

def aggregate_single_metrics(metrics_list: list) -> dict:
    """汇总单个标注者的指标"""
    total = {
        'correct': sum(m['correct'] for m in metrics_list),
        'incorrect': sum(m['incorrect'] for m in metrics_list),
        'partial': sum(m['partial'] for m in metrics_list),
        'missed': sum(m['missed'] for m in metrics_list),
        'spurious': sum(m['spurious'] for m in metrics_list),
        'actual': sum(m['actual'] for m in metrics_list),
        'possible': sum(m['possible'] for m in metrics_list)
    }
    
    total['precision'] = total['correct'] / total['actual'] if total['actual'] > 0 else 0
    total['recall'] = total['correct'] / total['possible'] if total['possible'] > 0 else 0
    
    if total['precision'] + total['recall'] > 0:
        total['f1'] = 2 * total['precision'] * total['recall'] / (total['precision'] + total['recall'])
    else:
        total['f1'] = 0

    return total

def evaluate_prediction(report_id: str, pred_entities: list, target_data: dict) -> tuple:
    """评估单个报告的预测结果"""
    # 获取真实数据
    true_data = target_data.get(report_id)
    if true_data is None:
        return None, False
        
    # 获取真实实体列表
    true_entities_list = get_entities_from_data(true_data)
    is_multi_labeler = len(true_entities_list) > 1
    
    # 转换预测结果为Entity格式
    pred_entities = convert_pred_to_entities(pred_entities)
    
    # 计算每组标注的指标
    metrics_list = []
    for true_entities in true_entities_list:
        y_true = entities_from_radgraph(true_entities)
        results, _ = compute_metrics(y_true, pred_entities, tags)
        metrics_list.append(results['strict'])
        
    return metrics_list, is_multi_labeler

def evaluate_all_predictions(pred_data: dict, target_data: dict) -> Tuple[dict, bool]:
    """评估所有预测结果并计算总体指标"""
    all_metrics = []
    is_multi_labeler = False
    
    # 遍历每个预测结果
    for report_id, pred_entities in pred_data.items():
        metrics, curr_multi_labeler = evaluate_prediction(
            report_id, 
            pred_entities, 
            target_data
        )
        
        if metrics is not None:
            is_multi_labeler = curr_multi_labeler
            all_metrics.append(metrics)
    
    # 计算总体指标
    total_metrics = aggregate_metrics(all_metrics, is_multi_labeler)
    
    return total_metrics, is_multi_labeler

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Evaluate NER predictions against ground truth')
    parser.add_argument('--prediction_path', type=str, required=True,
                      help='Path to the prediction results file')
    parser.add_argument('--target_path', type=str, required=True,
                      help='Path to the target/ground truth file')
    parser.add_argument('--output_dir', type=str, 
                      default='src/medkgc/ie/pipeline/ner/results',
                      help='Directory to save evaluation results')
    args = parser.parse_args()
    
    # 评估标签
    global tags
    tags = ['OBS-DP', 'ANAT-DP', 'OBS-U', 'OBS-DA']
    
    # 加载数据
    pred_data_json = load_json_data(args.prediction_path)
    target_data_json = load_json_data(args.target_path)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 从文件路径提取元数据
    model, shots, dataset_name = extract_metadata_from_paths(
        args.prediction_path, args.target_path)
    
    # 生成输出文件路径
    output_file = os.path.join(
        args.output_dir, 
        f'ner_eval_result_{model}_{shots}_{dataset_name}.txt'
    )
    
    # 执行评估
    total_metrics, is_multi_labeler = evaluate_all_predictions(pred_data_json, target_data_json)
    
    # 格式化并保存结果
    result_str = format_total_metrics(total_metrics, is_multi_labeler)
    
    # 保存到文件
    with open(output_file, 'w') as f:
        f.write(result_str)
    
    # 打印结果
    print(result_str)
    print(f'\n评估完成，结果已保存到 {output_file}')

if __name__ == '__main__':
    main()
