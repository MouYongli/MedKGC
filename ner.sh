#!/bin/bash
echo "Running Named Entity Recognition..."

# 运行预测脚本，可以通过命令行传入参数
nohup python -m src.medkgc.ie.pipeline.ner.predict \
    --num_shots 10 \
    --data_path "data/radgraph/original/test.json" > output.txt 2>&1 &

# 检查运行状态
if [ $? -eq 0 ]; then
    echo "NER prediction completed successfully!"
else
    echo "Error occurred during NER prediction!"
    exit 1
fi

tail -f output.txt
