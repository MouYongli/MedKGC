现在有了NER的结果，可以进行关系抽取了。

用LLMs进行关系抽取：
- 编写prompt
- 编写脚本
- 编写评估

从 `resource/radgraph/train.json` 中抽取数据作为few-shot示例。

`dev.json` 用于评估，评估结果将用于验证模型的性能。

### 代码结构

- `re.py`: 主要的执行文件，包含关系抽取的核心流程。
  - `load_shots`: 从训练数据中加载few-shot示例。
  - `format_shots`: 将示例格式化为prompt中需要的格式。
  - `extract_relations`: 使用LLM抽取实体间的关系。
  - `parse_llm_output`: 解析LLM输出的关系。
  - `evaluate_results`: 评估关系抽取结果。
  - `main`: 主函数，运行整个关系抽取流程。

- `utils.py`: 包含通用工具函数。
  - `setup_logging`: 配置日志输出。
  - `load_json`: 加载JSON文件。
  - `save_json`: 保存JSON文件。
  - `format_entities`: 格式化实体信息用于prompt。
  - `clean_text`: 清理文本。
  - `validate_relations`: 验证抽取的关系是否有效。

- `prompts.py`: 负责prompt管理。
  - `get_base_prompt`: 生成基础prompt。
  - `get_cot_prompt`: 生成chain-of-thought prompt。
  - `get_structured_prompt`: 生成结构化输出的prompt。

请根据需要完善各个模块的具体实现。

