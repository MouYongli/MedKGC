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
The system uses a few-shot learning approach with the following components:

1. System Prompt:
   - Defines the role as a radiologist
   - Specifies the task of clinical term extraction
   - Provides entity type definitions
   - Defines input/output format

2. Few-shot Examples:
   - Uses examples from RadGraph training data
   - Default: 50 examples per inference
   - Examples include text and corresponding entity annotations

3. Entity Extraction:
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
The evaluation process consists of the following steps:

1. Load RadGraph dev/test data
2. For each report:
   - Extract entities using LLM
   - Convert LLM output to standardized format
   - Compare with RadGraph ground truth
   - Compute precision, recall, and F1 scores

```python
# Example evaluation code
text = "Patient's lungs are clear..."
entities = extract_entities(text, num_shots=50)
pred = entities_from_llm_response(entities, text)
y_true = entities_from_radgraph(json_result)
metrics = compute_metrics(y_true, pred, tags)
```

## Usage
1. Ensure you have access to the LLM API endpoint
2. Run evaluation:
```bash
python ie/ner.py
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
