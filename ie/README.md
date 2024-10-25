# Information Extraction Project

## Overview
This project aims to extract named entities and relations from radiology reports, using the RadGraph dataset as input. The goal is to compare the performance of Large Language Models (LLMs) against the ground truth provided by RadGraph.

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

## LLM Output Format
LLMs produce named entities in a dictionary format:
```python
{
    'lungs': 'ANAT-DP',
    'clear': 'OBS-DP',
    'focal': 'OBS-DA',
    // ... more entities
}
```
LLMs may not handle entity offsets well, so additional processing is required.


## Key Functions

1. Process RadGraph data:
   ```python
   def entities_from_radgraph(json_result):
   ```

2. Process LLM output:
   ```python
   def extends_entities_offset(llm_result, text):

   def entities_from_llm_response(json_result, text):
   ```

3. Evaluation:
   ```python
   def compute_metrics(true_named_entities, pred_named_entities, tags):
   ```

## Evaluation Input Format
Both `true_named_entities` and `pred_named_entities` should be lists of `Entity` objects:
```python
[
    Entity(e_type='MISC', start_offset=12, end_offset=12),
    Entity(e_type='LOC', start_offset=15, end_offset=15),
    Entity(e_type='PER', start_offset=37, end_offset=39),
    Entity(e_type='ORG', start_offset=45, end_offset=46)
]
```
