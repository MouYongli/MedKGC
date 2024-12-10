from typing import Dict, List
import json
from utils import load_json, save_json, format_entities, setup_logging, validate_relations
from prompts import get_base_prompt, get_cot_prompt, get_structured_prompt

def load_shots(train_file: str, num_shots: int = 3) -> List[Dict]:
    """
    从训练数据中加载few-shot示例
    Args:
        train_file: 训练数据文件路径
        num_shots: 需要的示例数量
    Returns:
        示例列表
    """
    with open(train_file, 'r') as f:
        data = json.load(f)
    shots = []
    for i, (key, value) in enumerate(data.items()):
        if i >= num_shots:
            break
        shots.append(value)
    return shots

def format_shots(shots: List[Dict]) -> str:
    """
    将示例格式化为prompt中需要的格式
    Args:
        shots: 示例列表
    Returns:
        格式化后的示例字符串
    """
    formatted_shots = []
    for shot in shots:
        text = shot['text']
        entities = shot['entities']
        formatted_entities = format_entities(entities)
        formatted_shots.append(f"Text: {text}\nEntities: {formatted_entities}")
    return "\n\n".join(formatted_shots)

def extract_relations(text: str, entities: List[Dict], model, shots: str) -> List[Dict]:
    """
    使用LLM抽取实体间的关系
    Args:
        text: 输入文本
        entities: 实体列表
        model: LLM模型
        shots: 格式化后的few-shot示例
    Returns:
        关系列表
    """
    prompt = get_base_prompt(text, format_entities(entities), shots)
    response = model.generate(prompt)
    relations = parse_llm_output(response)
    return validate_relations(relations, entities)

def parse_llm_output(output: str) -> List[Dict]:
    """
    解析LLM输出的关系
    Args:
        output: LLM的输出文本
    Returns:
        结构化的关系列表
    """
    relations = []
    lines = output.strip().split('\n')
    for line in lines:
        if line:
            parts = line.split(',')
            if len(parts) == 3:
                relations.append({
                    'entity1': parts[0].strip(),
                    'relation': parts[1].strip(),
                    'entity2': parts[2].strip()
                })
    return relations

def evaluate_results(pred_relations: List[Dict], gold_relations: List[Dict]) -> Dict:
    """
    评估关系抽取结果
    Args:
        pred_relations: 预测的关系
        gold_relations: 金标关系
    Returns:
        评估指标
    """
    correct = 0
    for pred in pred_relations:
        if pred in gold_relations:
            correct += 1
    precision = correct / len(pred_relations) if pred_relations else 0
    recall = correct / len(gold_relations) if gold_relations else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def main(train_file: str, dev_file: str, output_file: str):
    """
    主函数，运行整个关系抽取流程
    """
    setup_logging()
    shots = load_shots(train_file)
    formatted_shots = format_shots(shots)
    
    dev_data = load_json(dev_file)
    results = []
    
    for item in dev_data:
        text = item['text']
        entities = item['entities']
        gold_relations = item['relations']
        
        pred_relations = extract_relations(text, entities, model=None, shots=formatted_shots)
        evaluation = evaluate_results(pred_relations, gold_relations)
        
        results.append({
            'text': text,
            'pred_relations': pred_relations,
            'gold_relations': gold_relations,
            'evaluation': evaluation
        })
    
    save_json(results, output_file)

if __name__ == "__main__":
    main(train_file='data/radgraph/original/train.json', 
         dev_file='data/radgraph/splits/dev_mimic.json', 
         output_file='results/re_results.json')
