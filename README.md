# Biomedical and Medical Knowledge Graph Construction - Named Entity Recognition & Normalization and Relation Extraction 

Access our online demo deployed on Hugging Face Spaces:  
[MedKGC Demo](https://huggingface.co/spaces/username/medkgc-demo)

![medkgc](medkgc.png)

## Project Story
This project focuses on Named Entity Recognition, Relation Extraction, and Named Entity Normalization in radiology, with the final output presented in the form of a knowledge graph.

The project implements these functionalities and provides methods for evaluation.

## Project Structure
The project is organized as follows:
```
MedKGC/
├── data/                   # Directory for storing datasets
│   ├── radgraph/          # RadGraph dataset and related files
│   └── radlex/            # RadLex terminology files
├── docs/                   # Project documentation
│   ├── index.html         # Documentation homepage
│   ├── ...               # Other documentation pages
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

2. environment variables
Set the home directory for Hugging Face:
```
export HF_HOME=~/Data/huggingface
```
3. project environment parameters

Set project environment parameters in the [.env](.env) file.

## Usage
Shell scripts are provided for direct execution.  
For example, ner.sh:
```
./ner.sh
```
You can set parameters and run directly; the program will make predictions, evaluate, and output results.  

## Run Tests
Run tests:
```
pytest ie/utils/test_ner.py -v
```
<details>
<summary>Detailed Information</summary>
`-v` - verbose mode, display detailed test output information
</details>

## Technology Stack
The project utilizes the following key technologies and tools:

- **Hugging Face Transformers**: Pre-trained models for NER and relation extraction
- **API calls**: Integration with UMLS API for entity normalization
- **Streamlit & Gradio**: For building interactive demonstration interfaces
- **Data processing**: Custom data cleaning and formatting pipeline
- **Hugging Face Dataset**: Project datasets published on the Hugging Face platform
- **Hugging Face Spaces**: Project demo deployed on Hugging Face Spaces
- **RAG with UMLS**: Combining retrieval-augmented generation with UMLS medical terminology

## Some Concepts
**mention / token**: a span of text in a report, which may or may not refer to an entity  
**entity**: result of NER, also a span of text in a report, which is recognized as a named entity  
**term**: a concept or standard form in a dictionary (e.g., UMLS).  

## Methods

本项目实现了一个完整的医学知识提取流程：

1. **端到端的医学知识提取流程**
   - 利用大型语言模型和**Hugging Face**库从放射学报告中提取医学知识
   - 构建了完整的处理管道，从原始文本到结构化知识图谱
   
2. **命名实体识别实现**
   - 使用**GPT-4o和Llama3**进行高精度医学实体识别
   - 采用创新的**RAG方法**集成UMLS医学术语知识
   - 实现了传统方法与大模型方法的结合，显著提升了性能

3. **知识整合与规范化**
   - 将识别出的实体与医学标准术语进行对齐
   - 构建结构化的医学知识图谱，支持临床应用

## Output
- Human annotated data as golden data, [dataset](nen/humanReview/reviewed.xlsx)
- Processed dataset published on [Hugging Face Datasets](https://huggingface.co/datasets/WestAI-SC/RadLink) 

## Experimental Results

### NER Task Results
我用 Llama 和 GPT-4o 在 NER 任务上做了实验，然后通过 entity-level 的 evaluation 得出了一系列实验结果:

![NER Results](nerResult.png)

上图展示了不同模型在实体识别任务上的性能对比，包括精确率、召回率和F1值等衡量指标。

### Few-shot Prompting Experiments

我们进行了**少样本提示**实验，以评估大语言模型在放射学文本上的性能：

- 测试了不同数量的示例对模型性能的影响
- 比较了不同提示策略的效果
- 分析了模型在医学领域专业术语上的理解能力

这些实验结果为临床环境中的模型选择和提示工程提供了重要见解，特别是在处理放射学文本这类专业医学内容时。

## Conclusions & Contributions

This project makes the following significant contributions to medical natural language processing and knowledge graph construction:

* **Comprehensive Evaluation** - Conducted a comparative assessment of specialized biomedical and general-purpose LLMs for radiological text processing, establishing performance benchmarks under various conditions
  
* **Enhanced Evaluation Framework** - Developed improved evaluation frameworks for assessing radiological NER and NEN performance, providing more nuanced performance metrics than traditional approaches
  
* **Annotated Corpus** - Created a manually annotated corpus of 1,250 entities mapped to standardized UMLS concepts, addressing a critical gap in available resources for this domain
  
* **Innovative RAG Architecture** - Implemented a novel retrieval-augmented generation architecture that effectively combines LLMs with established medical ontologies, showing significant performance improvements over traditional approaches
  
* **Practical Deployment Guidelines** - Provided insights into optimal model selection and configuration across varied data availability scenarios, offering practical guidance for clinical deployment of these technologies
