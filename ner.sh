#!/bin/bash
echo "Running Named Entity Recognition..."

# 运行预测脚本，可以通过命令行传入参数
python -m src.medkgc.ie.pipeline.ner.predict \
    --num_shots 100 \
    --start_index 0 \
    --data_path "data/radgraph/splits/dev_mimic.json" \
    --label_data_path "data/radgraph/splits/dev_mimic.json"

# 检查运行状态
if [ $? -eq 0 ]; then
    echo "NER prediction completed successfully!"
else
    echo "Error occurred during NER prediction!"
    exit 1
fi