import pytest
from .ner import extract_entities, create_messages_with_shots, get_question_prompt
import json
from unittest.mock import patch, MagicMock

# 模拟数据
MOCK_TRAIN_DATA = {
    "example1": {
        "text": "FINDINGS: There is a small right pleural effusion. No pneumothorax.\nIMPRESSION: Pleural effusion noted.",
        "entities": {
            "1": {"tokens": "right pleural effusion", "label": "OBS-DP"},
            "2": {"tokens": "pneumothorax", "label": "OBS-DA"}
        }
    }
}

@pytest.fixture
def mock_response():
    """模拟API响应的fixture"""
    return {
        "message": {
            "content": "('right pleural effusion', 'OBS-DP')\n('pneumothorax', 'OBS-DA')"
        }
    }

def test_get_question_prompt():
    """测试问题提示的格式是否正确"""
    test_text = "Sample text"
    expected_prompt = '''<INPUT>
        Sample text
        </INPUT> 

        What are the clinical terms and their labels in this text? Discard sections other than FINDINGS and IMPRESSION: eg. INDICATION, HISTORY, TECHNIQUE, COMPARISON sections. If there is no extraction from findings and impression, return (). Please only output the tuples without additional notes or explanations.

        <OUTPUT> ANSWER:
        '''
    assert get_question_prompt(test_text) == expected_prompt

@patch('builtins.open')
def test_create_messages_with_shots(mock_open):
    """测试few-shot示例消息创建"""
    # 模拟打开文件
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(MOCK_TRAIN_DATA)
    
    messages = [{'role': 'system', 'content': 'system prompt'}]
    result = create_messages_with_shots(1, messages)
    
    assert len(result) == 3  # system prompt + user message + assistant message
    assert result[1]['role'] == 'user'
    assert result[2]['role'] == 'assistant'

@patch('requests.Session')
def test_extract_entities(mock_session, mock_response):
    """测试实体提取功能"""
    # 模拟API响应
    mock_session.return_value.post.return_value.json.return_value = mock_response
    
    test_text = "FINDINGS: There is a small right pleural effusion. No pneumothorax."
    result = extract_entities(test_text, num_shots=1)
    
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['1']['tokens'] == 'right pleural effusion'
    assert result['1']['label'] == 'OBS-DP'
    assert result['2']['tokens'] == 'pneumothorax'
    assert result['2']['label'] == 'OBS-DA'

def test_extract_entities_invalid_response():
    """测试处理无效响应的情况"""
    with patch('requests.Session') as mock_session:
        # 模拟一个无效的响应格式
        mock_session.return_value.post.return_value.json.return_value = {
            "message": {
                "content": "invalid format response"
            }
        }
        
        result = extract_entities("test text", num_shots=1)
        assert isinstance(result, dict)
        assert len(result) == 0  # 应该返回空字典

def test_extract_entities_empty_text():
    """测试空文本输入的情况"""
    with patch('requests.Session') as mock_session:
        mock_session.return_value.post.return_value.json.return_value = {
            "message": {
                "content": "()"
            }
        }
        
        result = extract_entities("", num_shots=1)
        assert isinstance(result, dict)
        assert len(result) == 0 