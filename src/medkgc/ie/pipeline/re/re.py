from typing import Dict, List
import json
from utils import load_json, save_json, format_entities, setup_logging, validate_relations
from prompts import get_base_prompt, get_cot_prompt, get_structured_prompt
import logging

def load_shots(train_file: str, num_shots: int = 3) -> List[Dict]:
    """
    从训练数据中加载few-shot示例
    Args:
        train_file: 训练数据文件路径
        num_shots: 需要的示例数量
    Returns:
        示例列表
    """
    data = load_json(train_file)
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
        entities = format_entities(shot['entities'])
        relations = shot.get('relations', [])
        formatted_shots.append(f"Text: {text}\nEntities: {entities}\nRelations: {relations}\n")
    return "\n".join(formatted_shots)

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
    prompt = get_base_prompt(text, entities, shots)
    output = model.generate(prompt)
    relations = parse_llm_output(output)
    return relations

def parse_llm_output(output: str) -> List[Dict]:
    """
    解析LLM输出的关系
    Args:
        output: LLM的输出文本
    Returns:
        结构化的关系列表
    """
    relations = []
    lines = output.split('\n')
    for line in lines:
        if line.startswith('Relation:'):
            parts = line.split(',')
            relation_type = parts[0].split(':')[1].strip()
            source_entity = parts[1].split(':')[1].strip()
            target_entity = parts[2].split(':')[1].strip()
            relations.append({
                'relation_type': relation_type,
                'source_entity': source_entity,
                'target_entity': target_entity
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
    tp = 0
    fp = 0
    fn = 0
    for pred in pred_relations:
        if pred in gold_relations:
            tp += 1
        else:
            fp += 1
    for gold in gold_relations:
        if gold not in pred_relations:
            fn += 1
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
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
    logging.info("Loading few-shot examples...")
    shots = load_shots(train_file)
    formatted_shots = format_shots(shots)
    
    logging.info("Loading development data...")
    dev_data = load_json(dev_file)
    
    results = []
    for item in dev_data:
        text = item['text']
        entities = item['pred']
        gold_relations = item.get('relations', [])
        
        logging.info(f"Extracting relations for text: {text[:30]}...")
        pred_relations = extract_relations(text, entities, model=None, shots=formatted_shots)
        pred_relations = validate_relations(pred_relations, entities)
        
        result = {
            'text': text,
            'pred': entities,
            'relations': pred_relations,
            'gold_relations': gold_relations,
            'evaluation': evaluate_results(pred_relations, gold_relations)
        }
        results.append(result)
    
    logging.info(f"Saving results to {output_file}...")
    save_json(results, output_file)
    logging.info("Relation extraction completed.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run relation extraction")
    parser.add_argument("--train_file", type=str, required=True, help="Path to the training data file")
    parser.add_argument("--dev_file", type=str, required=True, help="Path to the development data file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save the output results")
    args = parser.parse_args()
    main(args.train_file, args.dev_file, args.output_file)
