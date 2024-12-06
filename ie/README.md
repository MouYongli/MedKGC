# Information Extraction Project

## Overview
This project aims to extract named entities from radiology reports using Large Language Models (LLMs) and compare their performance against the RadGraph dataset ground truth. The system focuses on identifying anatomical structures and medical observations with their presence status.

## Input Data
- Dataset: [RadGraph train_dev.json](../resource/radgraph/train_dev.json)
- Sample input text:
  ```
  FINAL REPORT EXAMINATION : CHEST ( PORTABLE AP ) INDICATION : ___ year old woman with SAH / / Fever workup Fever workup IMPRESSION : Compared to chest radiographs ___ . Patient has been extubated . Lungs are clear . Normal cardiomediastinal and hilar silhouettes and pleural surfaces .
  ```

## RadGraph Ground Truth Format
RadGraph provides entities and relations in the following JSON format:
```json
{
    "1": {
        "tokens": "Lungs",
        "label": "ANAT-DP",
        "start_ix": 36,
        "end_ix": 36,
        "relations": []
    },
    "2": {
        "tokens": "clear",
        "label": "OBS-DP",
        "start_ix": 38,
        "end_ix": 38,
        "relations": [
            [
                "located_at",
                "1"
            ]
        ]
    },
    // ... more entities
}
```

## Project Structure
```
ie/
├── ner.py              # Main evaluation script
├── utils/
│   ├── ner.py         # LLM entity extraction implementation
│   └── ner_eval.py    # Evaluation metrics computation
```

## Implementation Details

### LLM Entity Extraction
The system uses a few-shot learning approach with the following:
```python
def extract_entities(text, num_shots=50):
    """
    Extract named entities from radiology report text using LLM.
    Returns entities in format:
    {
        "1": {
            "tokens": "lungs",
            "label": "ANAT-DP"
        },
        ...
    }
    """
```

### Evaluation Pipeline
评估流程包含以下关键指标的计算：

1. 实体匹配评估：
- Correct Matches: 模型正确识别的实体数量
- Incorrect Matches: 模型识别错误的实体数量（标签错误）
- Missed Entities: 模型未能识别的实体数量（假阴性）
- Spurious Entities: 模型错误预测的额外实体（假阳性）

2. 性能指标计算：
- Precision (精确率): 
  - 正确预测的实体数量 / 模型预测的总实体数量
  - 衡量模型预测的准确性
- Recall (召回率):
  - 正确预测的实体数量 / 真实标注的总实体数量
  - 衡量模型发现实体的完整性
- F1 Score:
  - Precision 和 Recall 的调和平均数
  - 综合评估模型的整体性能

评估代码示例：
```python
# Example evaluation code
text = "Patient's lungs are clear..."
entities = extract_entities(text, num_shots=50)
pred = entities_from_llm_response(entities, text)

y_true = entities_from_radgraph(json_result)
metrics = compute_metrics(y_true, pred, tags)

# 输出结果示例：
# Overall Metrics:
# Total Correct: 464
# Total Incorrect: 176
# Total Missed: 1551
# Total Spurious: 127
# Precision: 0.6050
# Recall: 0.2118
# F1 Score: 0.3137
```

## Usage
1. Ensure you have access to the LLM API endpoint
2. Run evaluation:
```bash
nohup python ie/ner.py > output.log 2>&1 &
```

## Data
- Training data: `resource/radgraph/train.json`
- Development data: `resource/radgraph/dev.json`
- Test data: `resource/radgraph/test.json`

## Evaluation Metrics
The system evaluates entity extraction performance using:
- Precision
- Recall
- F1 Score

Results are computed for each entity type and aggregated for overall performance.

## TODO
- [ ] Implement relation extraction
- [ ] Optimize few-shot example selection
- [ ] Add support for additional LLM models
- [ ] Improve entity offset detection
