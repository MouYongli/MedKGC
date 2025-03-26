# RadGraph Dataset Structure

## Overview
RadGraph数据集包含了放射学报告的标注数据，主要包含实体(entities)和关系(relations)的标注。数据分为训练集(train)、开发集(dev)、测试集(test)等部分。

## 文件结构
- `train.json`: 训练集数据 (425条MIMIC数据)
- `dev.json`: 开发集数据 (75条MIMIC数据)
- `test.json`: 测试集数据 (50条MIMIC数据 + 50条CheXpert数据)

## 数据统计
按数据来源统计的样本数量：

| Dataset | MIMIC-CXR | CheXpert | Total |
|---------|-----------|----------|-------|
| train   | 425       | 0        | 425   |
| dev     | 75        | 0        | 75    |
| test    | 50        | 50       | 100   |
| Total   | 550       | 50       | 600   |

## training & dev 数据格式
每个文件包含多个报告的标注，每个报告的结构如下:

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
index 从 0 开始。

## test 数据格式
测试集中每个报告包含**两位专家标注者**(labeler_1和labeler_2)的标注:
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

注意:
1. 两位标注者可能对同一段文本有不同的实体识别和关系标注
2. 可以通过比较两位标注者的标注来评估标注的一致性

## 实体类型
- `ANAT-DP`: 解剖学描述性短语
- `OBS-DP`: 观察描述性短语
- `OBS-DA`: 观察异常性短语
- `OBS-U`: 不确定的观察

## 关系类型
主要的关系类型包括:
- `located_at`: 位置关系
- `modify`: 修饰关系
- `suggestive_of`: 提示关系

## 数据来源
- MIMIC-CXR
- CheXpert

## 特殊说明
1. test 数据包含2个标注者(labeler)的标注
2. 实体的位置使用token级别的start_ix和end_ix标注, not character级别的
3. 关系是有向的，主动的，从源实体指向目标实体
