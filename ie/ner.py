import utils.ner_eval as ner_eval
from utils.ner import extract_entities
import json

def main():
    # 加载测试数据
    with open('/home/hbchen/Projects/MedKGC/resource/radgraph/dev.json', 'r') as f:
        data = json.load(f)

    index = 0
    # 遍历每个样本进行评估
    for key, value in data.items():

        # 获取文本和标注实体
        text = value['text']
        json_result = value['entities']
        
        # 提取预测实体
        entities = extract_entities(text, num_shots=50)  # 移除shots_path参数,添加num_shots参数
        pred = ner_eval.entities_from_llm_response(entities, text)
        
        # 获取真实实体
        y_true = ner_eval.entities_from_radgraph(json_result)
        
        # 计算评估指标
        tag = ['OBS-DP', 'ANAT-DP', 'OBS-U', 'OBS-DA']
        result, evaluation_agg_entities_type = ner_eval.compute_metrics(y_true, pred, tag)
        
        print(f"Sample {key} evaluation result:")
        print(result['strict'])

if __name__ == '__main__':
    main()