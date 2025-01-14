目前是用dev的数据来eval结果，dev只有一个label。

```json
{
    "report_id": {
        "text": "报告的原始文本",
        "entities": {
            "entity_id": {
                "tokens": "实体文本",
                "label": "实体类型",
                "start_ix": 开始位置,
                "end_ix": 结束位置,
                "relations": [
                    ["关系类型", "目标实体ID"]
                ]
            }
        },
        "data_source": "数据来源",
        "data_split": "数据集划分"
    }
}
```


用test的数据来测试结果，test有2个label。
```json
{
    "report_id": {
        "text": "报告的原始文本",
        "labeler_1": {
            "entities": {
                "entity_id": {
                    "tokens": "实体文本",
                    "label": "实体类型",
                    "start_ix": 开始位置,
                    "end_ix": 结束位置,
                    "relations": [
                        ["关系类型", "目标实体ID"]
                    ]
                }
            },
            "data_source": "数据来源",
            "data_split": "数据集划分"
        },
        "labeler_2": {
            "entities": {
                "entity_id": {
                    "tokens": "实体文本",
                    "label": "实体类型",
                    "start_ix": 开始位置,
                    "end_ix": 结束位置,
                    "relations": [
                        ["关系类型", "目标实体ID"]
                    ]
                }
            },
            "data_source": "数据来源",
            "data_split": "数据集划分"
        },
        "data_source": "数据来源",
        "data_split": "数据集划分"
    }
}
```
我们把结果和每个labeler的结果都进行对比，然后计算两个labeler的平均结果。



要修改的是eval_ner.py里的代码。

目前eval_ner.py里的代码已经有计算结果和一组labels的F1。是将dev的predict和dev的label进行评估。dev只有一组label。

目前我有在文件夹test/里有几个结果，他是对test数据集的predict。
因为test有两组不同的labels。我需要把结果和两组labels都进行评估，然后计算F1，取平均值。

请你观察不同数据集，readme.md里的数据格式，然后修改eval_ner.py里的代码，计算test数据集的F1。