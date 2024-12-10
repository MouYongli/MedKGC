# Named Entity Recognition for Medical Reports

## Overview
This project aims to extract named entities from radiology reports using Large Language Models (LLMs) and compare their performance against the RadGraph dataset ground truth. The system focuses on identifying anatomical structures and medical observations with their presence status.

## Project Structure
```
MedKGC/
├── data/
│   └── radgraph/
│       ├── original/
│       │   └── train.json       # Original training data
│       ├── splits/
│       │   └── dev_mimic.json   # Development set
│       └── dev_mimic.json       # Ground truth for evaluation
├── src/
│   └── medkgc/
│       └── ie/
│           └── pipeline/
│               └── ner/
│                   ├── README.md
│                   ├── predict.py          # Main prediction script
│                   ├── eval_ner.py         # Evaluation script
│                   ├── utils/
│                   │   ├── entity_extractor.py  # LLM-based entity extraction
│                   │   └── ner_eval.py          # Evaluation metrics computation
│                   └── results/                 # Output directory for predictions
└── ner.sh          # Shell script for running the pipeline
```

## Usage

### Command Line Arguments
```bash
python -m src.medkgc.ie.pipeline.ner.predict \
    --num_shots 100 \            # Number of few-shot examples
    --start_index 0 \           # Start processing from this index
    --data_path "data/radgraph/splits/dev_mimic.json"  # Input data path
```

### Using Shell Script
```bash
./ner.sh
```

## Entity Types
- OBS-DP: Definite Positive Observations
- ANAT-DP: Definite Positive Anatomical Structures
- OBS-U: Uncertain Observations
- OBS-DA: Definite Absent Observations

## Output Format
The system generates predictions in JSON format:
```json
{
    "text": "Original report text...",
    "pred": [
        ["entity_type", start_index, end_index],
        ...
    ],
    "relations": [
        {"entity1": "entity1_text", "relation": "relation_type", "entity2": "entity2_text"},
        ...
    ]
}
```

## Evaluation Metrics
The system evaluates entity extraction and relation extraction performance using:
- Precision: Correct predictions / Total predictions
- Recall: Correct predictions / Total ground truth entities
- F1 Score: Harmonic mean of precision and recall

Results are saved in `results/ner_pred_{num_shots}.json`

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

## Relation Extraction
The system also extracts relations between entities using prompts and evaluates the results.

### Relation Extraction Functions
- `load_shots`: Load few-shot examples from `train.json`
- `format_shots`: Format examples for prompt
- `extract_relations`: Use LLM for relation extraction
- `parse_llm_output`: Parse LLM output into structured relations
- `evaluate_results`: Compare predicted and true relations

### Example Relation Extraction Code
```python
# Example relation extraction code
text = "Patient's lungs are clear..."
entities = extract_entities(text, num_shots=50)
formatted_shots = format_shots(load_shots('data/radgraph/original/train.json', num_shots=3))
relations = extract_relations(text, entities, model=None, shots=formatted_shots)

# Evaluate relations
gold_relations = [{"entity1": "lungs", "relation": "clear", "entity2": "lungs"}]
evaluation = evaluate_results(relations, gold_relations)

# 输出结果示例：
# Relation Extraction Metrics:
# Precision: 0.75
# Recall: 0.60
# F1 Score: 0.67
```

## Dependencies
- Python 3.10+
- LLaMA Model API
- Required Python packages (see requirements.txt)

## TODO
- [ ] Optimize few-shot example selection
- [ ] Add support for additional LLM models
- [ ] Improve entity offset detection
