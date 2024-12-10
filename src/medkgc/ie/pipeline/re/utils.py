from typing import Dict, List
import json
import logging

def setup_logging():
    """配置日志输出"""
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )

def load_json(file_path: str) -> Dict:
    """加载JSON文件"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: Dict, file_path: str):
    """保存JSON文件"""
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def format_entities(entities: List[Dict]) -> str:
    """
    格式化实体信息用于prompt
    Args:
        entities: 实体列表
    Returns:
        格式化后的实体字符串
    """
    formatted_entities = []
    for entity in entities:
        entity_type = entity[0]
        start_index = entity[1]
        end_index = entity[2]
        formatted_entities.append(f"{entity_type}({start_index}, {end_index})")
    return ", ".join(formatted_entities)

def clean_text(text: str) -> str:
    """
    清理文本
    Args:
        text: 输入文本
    Returns:
        清理后的文本
    """
    return text.replace('\n', ' ').replace('\r', '').strip()

def validate_relations(relations: List[Dict], entities: List[Dict]) -> List[Dict]:
    """
    验证抽取的关系是否有效
    Args:
        relations: 关系列表
        entities: 实体列表
    Returns:
        验证后的关系列表
    """
    valid_relations = []
    entity_set = set((e[1], e[2]) for e in entities)
    for relation in relations:
        source_entity = relation['source_entity']
        target_entity = relation['target_entity']
        if (source_entity[1], source_entity[2]) in entity_set and (target_entity[1], target_entity[2]) in entity_set:
            valid_relations.append(relation)
    return valid_relations
