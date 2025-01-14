#!/bin/bash
echo "开始评估命名实体识别结果..."

# 运行评估脚本
python -m src.medkgc.ie.pipeline.ner.eval_ner \
    --prediction_path "src/medkgc/ie/pipeline/ner/results/test/ner_pred_gpt4o_10.json" \
    --target_path "data/radgraph/original/test.json" \
    --output_dir "src/medkgc/ie/pipeline/ner/results/test/"

# 检查运行状态
if [ $? -eq 0 ]; then
    echo "NER评估完成!"
else
    echo "NER评估失败!"
    exit 1
fi 