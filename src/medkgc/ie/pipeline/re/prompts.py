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
    You are a medical information extraction model. Given the following text and entities, extract the relations between the entities.

    Few-shot examples:
    {shots}

    Text: {text}
    Entities: {entities}

    Extracted Relations (format: entity1, relation, entity2):
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
    You are a medical information extraction model. Given the following text and entities, extract the relations between the entities. Use chain-of-thought reasoning to explain your extraction process.

    Few-shot examples:
    {shots}

    Text: {text}
    Entities: {entities}

    Chain-of-Thought Reasoning:
    1. Identify the entities in the text.
    2. Determine the possible relations between the entities.
    3. Extract the relations based on the context.

    Extracted Relations (format: entity1, relation, entity2):
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
    You are a medical information extraction model. Given the following text and entities, extract the relations between the entities and provide the output in a structured format.

    Few-shot examples:
    {shots}

    Text: {text}
    Entities: {entities}

    Extracted Relations (format: entity1, relation, entity2):
    """
    return prompt
