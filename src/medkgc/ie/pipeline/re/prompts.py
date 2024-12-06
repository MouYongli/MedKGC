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
    pass

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
    pass

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
    pass