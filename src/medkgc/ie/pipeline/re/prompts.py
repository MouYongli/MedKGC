from typing import Dict, List

def get_base_prompt(text: str, entities: str, shots: str) -> str:
    """
    生成基础prompt
    Args:
        text: 输入文本
        entities: 格式化后的实体信息
        shots: few-shot示例
    Returns:
        完整的prompt
    """
    prompt = f"""
    You are a medical expert. Given the following text and entities, identify the relations between the entities.

    Text: {text}

    Entities: {entities}

    Few-shot examples:
    {shots}

    Please provide the relations in the format: (relation_type, source_entity, target_entity)
    """
    return prompt

def get_cot_prompt(text: str, entities: str, shots: str) -> str:
    """
    生成chain-of-thought prompt
    Args:
        text: 输入文本
        entities: 格式化后的实体信息
        shots: few-shot示例
    Returns:
        完整的prompt
    """
    prompt = f"""
    You are a medical expert. Given the following text and entities, identify the relations between the entities. Use chain-of-thought reasoning to explain your process.

    Text: {text}

    Entities: {entities}

    Few-shot examples:
    {shots}

    Please provide the relations in the format: (relation_type, source_entity, target_entity) and explain your reasoning.
    """
    return prompt

def get_structured_prompt(text: str, entities: str, shots: str) -> str:
    """
    生成结构化输出的prompt
    Args:
        text: 输入文本
        entities: 格式化后的实体信息
        shots: few-shot示例
    Returns:
        完整的prompt
    """
    prompt = f"""
    You are a medical expert. Given the following text and entities, identify the relations between the entities. Provide the output in a structured format.

    Text: {text}

    Entities: {entities}

    Few-shot examples:
    {shots}

    Please provide the relations in the format: (relation_type, source_entity, target_entity) in a structured JSON format.
    """
    return prompt
