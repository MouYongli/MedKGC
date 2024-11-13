import pytest
from ie.utils.ner_eval import entities_from_radgraph, entities_from_llm_response, Entity

def test_entities_from_radgraph():
    """测试从RadGraph格式JSON转换为Entity对象"""
    # 准备测试数据
    test_json = {
        "1": {
            "label": "OBS-DP",
            "start_ix": 5,
            "end_ix": 7,
            "tokens": "pleural effusion"
        },
        "2": {
            "label": "ANAT-DP",
            "start_ix": 10,
            "end_ix": 10,
            "tokens": "lung"
        }
    }
    
    # 执行测试
    entities = entities_from_radgraph(test_json)
    
    # 验证结果
    assert len(entities) == 2
    assert isinstance(entities[0], Entity)
    assert entities[0].e_type == "OBS-DP"
    assert entities[0].start_offset == 5
    assert entities[0].end_offset == 7
    assert entities[1].e_type == "ANAT-DP"
    assert entities[1].start_offset == 10
    assert entities[1].end_offset == 10

def test_entities_from_radgraph_empty():
    """测试空JSON输入的情况"""
    empty_json = {}
    entities = entities_from_radgraph(empty_json)
    assert len(entities) == 0
    assert isinstance(entities, list)

def test_entities_from_llm_response():
    """测试从LLM响应转换为Entity对象"""
    # 准备测试数据
    test_json = {
        "1": {
            "tokens": "effusion",
            "label": "OBS-DP"
        },
        "2": {
            "tokens": "lung",
            "label": "ANAT-DP"
        }
    }
    test_text = "There is pleural effusion in the right lung base"
    
    # 执行测试
    entities = entities_from_llm_response(test_json, test_text)
    
    # 验证结果
    assert len(entities) == 2
    assert isinstance(entities[0], Entity)
    assert entities[0].e_type == "OBS-DP"
    assert entities[1].e_type == "ANAT-DP"

def test_entities_from_llm_response_token_not_found():
    """测试当token在文本中找不到时的情况"""
    test_json = {
        "1": {
            "tokens": "nonexistent",
            "label": "OBS-DP"
        }
    }
    test_text = "Normal text without the token"
    
    entities = entities_from_llm_response(test_json, test_text)
    assert len(entities) == 0

def test_entities_from_llm_response_empty():
    """测试空输入的情况"""
    empty_json = {}
    test_text = "Some text"
    entities = entities_from_llm_response(empty_json, test_text)
    assert len(entities) == 0
    assert isinstance(entities, list)

def test_entities_from_llm_response_multiple_occurrences():
    """测试文本中有多个相同token的情况"""
    test_json = {
        "1": {
            "tokens": "the",
            "label": "MISC"
        }
    }
    test_text = "the cat and the dog"
    
    entities = entities_from_llm_response(test_json, test_text)
    # 应该只匹配第一次出现的位置
    assert len(entities) == 1
    assert entities[0].start_offset == 0
    assert entities[0].end_offset == 0

def test_entities_from_llm_response_case_sensitive():
    """测试大小写敏感性"""
    test_json = {
        "1": {
            "tokens": "Lung",
            "label": "ANAT-DP"
        }
    }
    test_text = "lung disease"  # 注意大小写不同
    
    entities = entities_from_llm_response(test_json, test_text)
    assert len(entities) == 0  # 因为大小写不匹配，所以找不到

@pytest.mark.parametrize("test_input,expected", [
    # 测试不同类型的标签
    ({"1": {"tokens": "lung", "label": "ANAT-DP"}}, "ANAT-DP"),
    ({"1": {"tokens": "effusion", "label": "OBS-DP"}}, "OBS-DP"),
    ({"1": {"tokens": "maybe", "label": "OBS-U"}}, "OBS-U"),
])
def test_entities_from_llm_response_different_labels(test_input, expected):
    """测试不同类型的标签"""
    test_text = "lung effusion maybe"
    entities = entities_from_llm_response(test_input, test_text)
    assert len(entities) == 1
    assert entities[0].e_type == expected 