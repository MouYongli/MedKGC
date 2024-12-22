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


## todo
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