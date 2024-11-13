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

import utils.ner_eval as ner_eval
from utils.ner import extract_entities
import json

def main():
    '''predict the radgraph dataset using the llm, then save the result'''
    
    # 加载测试数据，dev有75个样本
    with open('/home/hbchen/Projects/MedKGC/resource/radgraph/dev.json', 'r') as f:
        data = json.load(f)

    json_result_list = []
    file_path = 'ie/outputs/ner_pred.json'

    index = 0
    # 遍历每个样本进行评估
    for key, value in data.items():
        # 获取文本和标注实体
        text = value['text']
        json_result = value['entities']
        
        # 提取预测实体
        # NOTE: 这里使用50个示例，可以修改
        entities = extract_entities(text, num_shots=50)
        pred = ner_eval.entities_from_llm_response(entities, text)
        
        # 保存结果（text, pred）
        json_result_list.append({'text': text, 'pred': pred})
        
        # 每处理一个样本就保存一次结果
        with open(file_path, 'w') as f:
            json.dump(json_result_list, f)
            
        index += 1
        print(f'已处理 {index} 个样本')

if __name__ == '__main__':
    main()