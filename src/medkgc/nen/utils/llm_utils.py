import os
import json
from openai import OpenAI

# 提取系统消息为常量
SYSTEM_MESSAGE = "You are an expert in named entity normalization for medical terms using the UMLS ontology. Your task is to analyze the given entity and search results, then select the most appropriate normalized form or the most likely UMLS concept."

# 新增：构造 user message 的函数
def build_user_message(entity, results) -> dict:
    results_str = json.dumps(results, indent=2)
    content = (
        f"Entity: {entity}\n\nSearch Results:\n{results_str}\n\n"
        "Based on these results, provide the most appropriate UI and name for this entity. "
        "If the entity is unlikely to be normalized, return ('unnormalizable', 'unnormalizable'). "
        "Respond in the format: (ui, name)"
    )
    return {"role": "user", "content": content}

def normalize_entity_gpt(entity, results, myModel="gpt-4"):
    # Initialize the OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # 构造消息列表，使用新增的 build_user_message 函数
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        build_user_message(entity, results)
    ]

    # Make the API call
    completion = client.chat.completions.create(
        model=myModel,
        messages=messages
    )

    # Extract and process the response
    response = completion.choices[0].message.content.strip()

    try:
        ui, name = eval(response)
    except:
        ui, name = None, None

    return ui, name
