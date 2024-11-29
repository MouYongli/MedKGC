import json
import os

def split_by_source(input_file, output_dir):
    """
    将输入的json文件按照数据来源(CheXpert/MIMIC)分割成独立的文件
    
    Args:
        input_file: 输入json文件的路径
        output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取输入文件
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # 准备两个字典来存储不同来源的数据
    chexpert_data = {}
    mimic_data = {}
    
    # 遍历数据
    for report_id, report_content in data.items():
        # 处理测试集的特殊情况（包含多个标注者）
        if 'labeler_1' in report_content:
            source = report_content['data_source'].lower()
        else:
            source = report_content.get('data_source', '').lower()
            
        # 根据来源分配数据
        if 'chexpert' in source:
            chexpert_data[report_id] = report_content
        elif 'mimic' in source:
            mimic_data[report_id] = report_content
    
    # 获取输入文件的基本名称（不包含扩展名）
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 保存分割后的文件
    chexpert_file = os.path.join(output_dir, f'{base_name}_chexpert.json')
    mimic_file = os.path.join(output_dir, f'{base_name}_mimic.json')
    
    with open(chexpert_file, 'w') as f:
        json.dump(chexpert_data, f, indent=2)
    
    with open(mimic_file, 'w') as f:
        json.dump(mimic_data, f, indent=2)
        
    return len(chexpert_data), len(mimic_data)

def main():
    # 设置基础路径
    base_dir = os.path.join('resource', 'radgraph')
    input_files = ['train.json', 'dev.json', 'test.json']
    output_dir = os.path.join(base_dir, 'split_data')
    
    for input_file in input_files:
        input_path = os.path.join(base_dir, input_file)
        print(f'处理文件: {input_file}')
        chexpert_count, mimic_count = split_by_source(input_path, output_dir)
        print(f'- CheXpert数据条数: {chexpert_count}')
        print(f'- MIMIC数据条数: {mimic_count}')
        print()

if __name__ == '__main__':
    main()
