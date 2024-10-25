
# Biomedical and Medical Knowledge Graph Construction - Named Entity Recognition & Normalization and Relation Extraction 

## Dataset Setup

Existing Dictionaries
- UMLS: Snomed CT, MeSH

## Python Environment Setup

1. conda environment
```
conda create --name=medkgc python=3.10
conda activate medkgc
```

```
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1
pip install torch_geometric
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.2.0+cu121.html
pip install -r requirements.txt
pip install -e .
```

2. jupyter lab and kernel
```
conda install -c conda-forge jupyterlab
conda install ipykernel
ipython kernel install --user --name=medkgc
```

exit and reopen a session (conda env medkgc)

```
jupyter lab --no-browser --port=8888
```

3. enviroment variables
```
export HF_HOME=~/Data/huggingface
```

## Some Concepts
mention / token: a span of text in a report, which may or may not refer to an entity
entity: resulf of NER, also a span of text in a report, which be recognized as a named entity
term: a concept or standard form in a dictionary(e.g. UMLS).


## Output
- Human annotated data as golden data, [dataset](nen/humanReview/reviewed.xlsx)

# Project Story
A automated annotion tool using LLMs to help medical annotators annotate the input radiology reports.  

这个工具涉及了Named Entity Recognition，relation extraction, named entity normalization，最终结果会以知识图谱的形式输出。

