from typing import Dict, Optional
from .utils.umls_api import nomralize_entity_with_umls, nomralize_entity_with_umls_and_gpt

def normalize_entity(entity: str, use_gpt: bool = False) -> Optional[Dict]:
    """
    将输入的医疗实体标准化，返回其UMLS标准信息
    
    Args:
        entity: 输入的医疗实体文本
        use_gpt: 是否使用GPT来辅助标准化，默认为False
    
    Returns:
        包含标准化信息的字典，如果标准化失败则返回None
        {
            "entity": 原始实体文本,
            "ui": UMLS概念唯一标识符,
            "term": UMLS标准术语,
            "semanticTypes": 语义类型,
            "definition": 定义,
            "source": 来源
        }
    """
    if not entity or not isinstance(entity, str):
        return None
        
    # 根据use_gpt参数选择不同的标准化方法
    if use_gpt:
        entity, ui, term, semantic_types, definition, source = nomralize_entity_with_umls_and_gpt(entity)
    else:
        entity, ui, term, semantic_types, definition, source = nomralize_entity_with_umls(entity)
    
    # 如果标准化失败，返回None
    if entity is None:
        return None
        
    # 构建返回的字典
    result = {
        "entity": entity,
        "ui": ui,
        "term": term,
        "semanticTypes": semantic_types,
        "definition": definition,
        "source": source
    }
    
    return result

