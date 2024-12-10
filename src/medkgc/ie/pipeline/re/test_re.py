import pytest
from re import load_shots, format_shots, extract_relations, parse_llm_output, evaluate_results

def test_load_shots():
    """测试从训练数据中加载few-shot示例"""
    train_file = 'data/radgraph/train.json'
    num_shots = 3
    shots = load_shots(train_file, num_shots)
    assert len(shots) == num_shots
    assert isinstance(shots, list)
    assert isinstance(shots[0], dict)

def test_format_shots():
    """测试将示例格式化为prompt中需要的格式"""
    shots = [
        {
            "text": "Sample text 1",
            "entities": [
                ["entity_type_1", 0, 10],
                ["entity_type_2", 15, 25]
            ],
            "relations": [
                ["relation_type_1", "entity_1", "entity_2"]
            ]
        },
        {
            "text": "Sample text 2",
            "entities": [
                ["entity_type_3", 5, 20]
            ],
            "relations": [
                ["relation_type_2", "entity_3", "entity_4"]
            ]
        }
    ]
    formatted_shots = format_shots(shots)
    assert isinstance(formatted_shots, str)
    assert "Sample text 1" in formatted_shots
    assert "entity_type_1(0, 10)" in formatted_shots
    assert "relation_type_1" in formatted_shots

def test_extract_relations():
    """测试使用LLM抽取实体间的关系"""
    text = "Sample text"
    entities = [
        ["entity_type_1", 0, 10],
        ["entity_type_2", 15, 25]
    ]
    model = None  # 模拟模型
    shots = "Sample shots"
    relations = extract_relations(text, entities, model, shots)
    assert isinstance(relations, list)
    assert isinstance(relations[0], dict)

def test_parse_llm_output():
    """测试解析LLM输出的关系"""
    output = """
    Relation: relation_type_1, Source: entity_1, Target: entity_2
    Relation: relation_type_2, Source: entity_3, Target: entity_4
    """
    relations = parse_llm_output(output)
    assert isinstance(relations, list)
    assert len(relations) == 2
    assert relations[0]['relation_type'] == 'relation_type_1'
    assert relations[0]['source_entity'] == 'entity_1'
    assert relations[0]['target_entity'] == 'entity_2'

def test_evaluate_results():
    """测试评估关系抽取结果"""
    pred_relations = [
        {"relation_type": "relation_type_1", "source_entity": "entity_1", "target_entity": "entity_2"},
        {"relation_type": "relation_type_2", "source_entity": "entity_3", "target_entity": "entity_4"}
    ]
    gold_relations = [
        {"relation_type": "relation_type_1", "source_entity": "entity_1", "target_entity": "entity_2"},
        {"relation_type": "relation_type_3", "source_entity": "entity_5", "target_entity": "entity_6"}
    ]
    evaluation = evaluate_results(pred_relations, gold_relations)
    assert isinstance(evaluation, dict)
    assert 'precision' in evaluation
    assert 'recall' in evaluation
    assert 'f1' in evaluation
