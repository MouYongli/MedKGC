# Biomedical and Medical Knowledge Graph Construction - Named Entity Recognition & Normalization and Relation Extraction 

## Project Story
这个项目设计在radiology中的Named Entity Recognition，relation extraction, named entity normalization，最终结果会以知识图谱的形式输出。

项目实现了上述的功能，并提供了evaluation的方法。

## Project Structure
The project is organized as follows:
```
MedKGC/
├── data/                   # Directory for storing datasets
│   ├── radgraph/          # RadGraph dataset and related files
│   └── radlex/            # RadLex terminology files
├── docs/                   # Project documentation
│   ├── index.html         # Documentation homepage
│   ├── ...               # 其他文档页面
│   └── assets/            # Static assets for documentation
├── notebooks/              # Jupyter notebooks for experiments and analysis
├── src/                    # Source code for the project
│   └── medkgc/             # Main package for the project
│       ├── ie/             # Information extraction related code
│       │   ├── pipeline/   # Pipeline for NER, normalization, and relation extraction
│       │   │   ├── ner/    # Named Entity Recognition
│       │   │   ├── re/     # Relation Extraction
│       │   │   └── nen/    # Named Entity Normalization
│       │   └── utils/      # Utility functions and scripts
│       └── nen/            # Named Entity Normalization specific code
│           ├── resource/   # Resources for normalization
│           └── notebooks/  # NEN analysis notebooks
├── tests/                  # Unit tests for the project
├── requirements.txt        # Python dependencies
├── setup.py                # Package installation configuration
└── README.md               # Project documentation
```

## Dataset Setup

Existing Dictionaries
- UMLS: Snomed CT, MeSH

## Python Environment Setup

1. conda environment
```
conda create --name=medkgc python=3.10
conda activate medkgc
pip install -r requirements.txt
```

2. enviroment variables
设置huggingface的home目录。
```
export HF_HOME=~/Data/huggingface
```
3. 项目环境参数

设置项目环境参数在[.env](.env)文件中。

## Usage
提供了.sh文件，可以直接运行。  
比如ner.sh
```
./ner.sh
```
可以设置参数，直接运行，程序会进行预测，评估，输出结果。  




## Run Tests
Run tests:
```
pytest ie/utils/test_ner.py -v
```
<details>
<summary>Detailed Information</summary>
`-v` - verbose mode, display detailed test output information
</details>




## Some Concepts
**mention / token**: a span of text in a report, which may or may not refer to an entity  
**entity**: resulf of NER, also a span of text in a report, which be recognized as a named entity  
**term**: a concept or standard form in a dictionary(e.g. UMLS).  


## Output
- Human annotated data as golden data, [dataset](nen/humanReview/reviewed.xlsx)

## Demo
![medkgc](medkgc.png)
