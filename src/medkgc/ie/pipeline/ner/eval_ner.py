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
    python -m src.medkgc.ie.pipeline.ner.eval_ner \
        --prediction_path src/medkgc/ie/pipeline/ner/results/ner_pred_gpt4_100.json \
        --target_path data/radgraph/splits/dev_mimic.json

输出文件：
    src/medkgc/ie/pipeline/ner/results/ner_eval_result.txt
"""

import json
import argparse
import os
from medkgc.ie.pipeline.ner.utils.ner_metrics import Entity, compute_metrics, entities_from_radgraph
import sys

def load_json_data(file_path: str) -> dict:
    """加载ner的结果文件，predict.JSON数据文件"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'错误: 找不到数据文件 {file_path}')
        sys.exit(1)

def get_entities_from_data(data_item: dict) -> list:
    """
    根据数据格式返回entities列表
    
    Args:
        data_item: 数据项，可能包含单个entities或多个labeler的entities
        
    Returns:
        list: 包含一个或多个entities列表
    """
    if 'entities' in data_item:
        return [data_item['entities']]
    elif 'labeler_1' in data_item and 'labeler_2' in data_item:
        return [data_item['labeler_1']['entities'], 
                data_item['labeler_2']['entities']]
    else:
        raise ValueError("未知的数据格式：既没有entities也没有labeler标注")

def aggregate_metrics(metrics_list: list, is_multi_labeler: bool = False) -> dict:
    """
    汇总评估指标
    
    Args:
        metrics_list: 指标列表
        is_multi_labeler: 是否多标注者
        
    Returns:
        dict: 汇总的指标
    """
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
    """原来的aggregate_metrics函数逻辑"""
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

def convert_pred_to_entities(pred_result: list) -> list:
    """
    将预测结果转换为Entity格式
    
    Args:
        pred_result: 格式为 [[label, start, end], ...] 的预测结果
        
    Returns:
        list[Entity]: 转换后的Entity列表
    """
    entities = []
    
    # 遍历每个预测结果
    for item in pred_result:
        entity = Entity(e_type=item[0], 
                      start_offset=item[1], 
                      end_offset=item[2])
        entities.append(entity)
        
    return entities

def write_metrics(f, metrics: dict, prefix: str = ''):
    """写入评估指标到文件"""
    f.write(f"{prefix}正确预测数: {metrics['correct']}\n")
    f.write(f"{prefix}错误预测数: {metrics['incorrect']}\n")
    f.write(f"{prefix}未预测数: {metrics['missed']}\n")
    f.write(f"{prefix}多余预测数: {metrics['spurious']}\n")
    f.write(f"{prefix}精确率: {metrics['precision']:.4f}\n")
    f.write(f"{prefix}召回率: {metrics['recall']:.4f}\n")
    f.write(f"{prefix}F1分数: {metrics['f1']:.4f}\n")

def setup_evaluation(args):
    """
    设置评估环境并加载数据
    
    Args:
        args: 解析的命令行参数
        
    Returns:
        tuple: (target_data, pred_data, output_file)
    """
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 加载数据
    pred_data = load_json_data(args.prediction_path)
    target_data = load_json_data(args.target_path)
    
    # 生成输出文件路径
    output_file = os.path.join(args.output_dir, 'ner_eval_result.txt')
    
    return target_data, pred_data, output_file

def evaluate_all_predictions(pred_data: dict, target_data: dict, output_file: str):
    """
    评估所有预测结果并计算总体指标
    
    Args:
        pred_data: 预测结果字典 {report_id: [[label, start, end], ...]}
        target_data: 目标数据字典
        output_file: 输出文件路径
        
    Returns:
        tuple: (total_metrics, is_multi_labeler)
    """
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
    
    # 将总体指标写入文件
    with open(output_file, 'w') as f:
        write_total_metrics(f, total_metrics, is_multi_labeler)
    
    return total_metrics, is_multi_labeler

def evaluate_prediction(report_id: str, pred_entities: list, target_data: dict) -> tuple:
    """
    评估单个报告的预测结果

    Returns:
        tuple: (metrics_list, is_multi_labeler)
        - metrics_list: 评估指标列表，可能包含多个标注者的指标
        - is_multi_labeler: 是否为多标注者数据
    """
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

def write_total_metrics(f, total_metrics, is_multi_labeler):
    """
    写入总体评估指标
    """
    f.write("总体评估指标:\n")
    
    if is_multi_labeler:
        f.write("\n标注者 1 结果:\n")
        write_metrics(f, total_metrics['labeler_1'])
        f.write("\n标注者 2 结果:\n")
        write_metrics(f, total_metrics['labeler_2'])
        f.write(f"\n平均F1分数: {total_metrics['avg_f1']:.4f}\n")
    else:
        write_metrics(f, total_metrics)

def print_total_metrics(total_metrics, is_multi_labeler):
    """
    在终端打印总体评估指标
    """
    print("\n总体评估指标:")
    if is_multi_labeler:
        print("\n标注者 1 结果:")
        write_metrics(sys.stdout, total_metrics['labeler_1'])
        print("\n标注者 2 结果:")
        write_metrics(sys.stdout, total_metrics['labeler_2'])
        print(f"\n平均F1分数: {total_metrics['avg_f1']:.4f}")
    else:
        write_metrics(sys.stdout, total_metrics)

if __name__ == '__main__':
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
    tags = ['OBS-DP', 'ANAT-DP', 'OBS-U', 'OBS-DA']
    
    # 设置评估环境并加载数据
    target_data, pred_data, output_file = setup_evaluation(args)
    
    # 执行评估并获取结果
    total_metrics, is_multi_labeler = evaluate_all_predictions(
        pred_data, target_data, output_file)
    
    # 在终端显示结果
    print_total_metrics(total_metrics, is_multi_labeler)

    print(f'\n评估完成，结果已保存到 {output_file}')
