"""
NER评估脚本

这个脚本用于评估命名实体识别(NER)的预测结果。主要功能包括：

1. 读取数据：
   - 加载开发集(dev.json)作为真实标注
   - 加载预测结果(ner_pred.json)
   
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
    python ie/eval_ner.py

输出格式：
    对每个报告输出其precision和recall
    最后输出总体评估指标
"""

import json
from medkgc.ie.pipeline.ner.utils.ner_eval import Entity, compute_metrics, entities_from_radgraph
import argparse
import time

def load_dev_data(label_data_path):
    """加载开发集数据"""
    with open(label_data_path, 'r') as f:
        return json.load(f)

def load_pred_data(shots=50):
    """加载预测结果"""
    with open(f'src/medkgc/ie/pipeline/ner/results/ner_pred_{shots}.json', 'r') as f:
        return json.load(f)

def aggregate_metrics(metrics_list):
    """汇总多个报告的指标"""
    total = {
        'correct': sum(m['correct'] for m in metrics_list),
        'incorrect': sum(m['incorrect'] for m in metrics_list),
        'partial': sum(m['partial'] for m in metrics_list),
        'missed': sum(m['missed'] for m in metrics_list),
        'spurious': sum(m['spurious'] for m in metrics_list),
        'actual': sum(m['actual'] for m in metrics_list),
        'possible': sum(m['possible'] for m in metrics_list)
    }
    
    # 计算总体精确率和召回率
    total['precision'] = total['correct'] / total['actual'] if total['actual'] > 0 else 0
    total['recall'] = total['correct'] / total['possible'] if total['possible'] > 0 else 0
    
    # 计算F1分数
    if total['precision'] + total['recall'] > 0:
        total['f1'] = 2 * total['precision'] * total['recall'] / (total['precision'] + total['recall'])
    else:
        total['f1'] = 0

    return total

def convert_pred_to_entities(pred_result):
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
        e_type = item[0]  # 第一个元素是标签类型
        start_offset = item[1]  # 第二个元素是起始位置
        end_offset = item[2]  # 第三个元素是结束位置
        
        # 创建Entity对象并添加到列表中
        entity = Entity(e_type=e_type, 
                      start_offset=start_offset, 
                      end_offset=end_offset)
        entities.append(entity)
    
    return entities

def main(num_shots=50, label_data_path='data/radgraph/splits/dev_mimic.json'):
    # 加载数据
    dev_data = load_dev_data(label_data_path)
    pred_data = load_pred_data(num_shots)
    
    # 评估标签
    tags = ['OBS-DP', 'ANAT-DP', 'OBS-U', 'OBS-DA']
    
    # 存储每个报告的指标
    all_metrics = []
    
    # 创建结果输出文件
    output_file = f'src/medkgc/ie/pipeline/ner/results/ner_pred_result_{num_shots}.txt'

    with open(output_file, 'w') as f:
        # 遍历每个预测结果
        for i, pred_item in enumerate(pred_data):
            text = pred_item['text']
            pred_result = pred_item['pred']
            
            # 获取对应的真实标注
            true_entities = None
            for key, value in dev_data.items():
                if value['text'] == text:
                    true_entities = value['entities']
                    break
            
            if true_entities is None:
                f.write(f"Warning: Could not find true entities for report {i}\n")
                continue
                
            # 转换为Entity格式
            y_true = entities_from_radgraph(true_entities)
            y_pred = convert_pred_to_entities(pred_result)
            
            # 计算指标
            results, _ = compute_metrics(y_true, y_pred, tags)
            all_metrics.append(results['strict'])
            
            # 将每个报告的指标写入文件
            f.write(f"\nReport {i+1}:\n")
            f.write(f"Precision: {results['strict']['precision']:.4f}\n")
            f.write(f"Recall: {results['strict']['recall']:.4f}\n")
        
        # 计算汇总指标
        total_metrics = aggregate_metrics(all_metrics)
        
        # 将总体指标写入文件
        f.write("\n" + "="*50 + "\n")
        f.write("Overall Metrics:\n")
        f.write(f"Total Correct: {total_metrics['correct']}\n")
        f.write(f"Total Incorrect: {total_metrics['incorrect']}\n")
        f.write(f"Total Missed: {total_metrics['missed']}\n")
        f.write(f"Total Spurious: {total_metrics['spurious']}\n")
        f.write(f"Precision: {total_metrics['precision']:.4f}\n")
        f.write(f"Recall: {total_metrics['recall']:.4f}\n")
        f.write(f"F1 Score: {total_metrics['f1']:.4f}\n")
    
    # 在终端也显示总体指标
    print("\nOverall Metrics:")
    print(f"Total Correct: {total_metrics['correct']}")
    print(f"Total Incorrect: {total_metrics['incorrect']}")
    print(f"Total Missed: {total_metrics['missed']}")
    print(f"Total Spurious: {total_metrics['spurious']}")
    print(f"Precision: {total_metrics['precision']:.4f}")
    print(f"Recall: {total_metrics['recall']:.4f}")
    print(f"F1 Score: {total_metrics['f1']:.4f}")

    print(f'评估完成，结果已保存到 {output_file}')

if __name__ == '__main__':
    main(num_shots=10, label_data_path='data/radgraph/splits/dev_mimic.json')