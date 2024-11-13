import json
import requests
import pprint


# Prepare prompt with instructions
system_prompt = '''You are a radiologist performing clinical term extraction from the FINDINGS and IMPRESSION sections 
    in the radiology report. Here a clinical term can be either anatomy or observation that is related to a finding or an impression. The anatomy term refers to an anatomical body part such as a 'lung'. The observation terms refer to observations made when referring to the associated radiology image. Observations are associated with visual features, identifiable pathophysiologic processes, or diagnostic disease classifications. For example, an observation could be 'effusion' or description phrases like 'increased'. You also need to assign a label to indicate whether the clinical term is present, absent or uncertain. The labels are:
    - OBS-DP: Observation definitely present
    - ANAT-DP: Anatomy definitely present  
    - OBS-U: Observation uncertain
    - OBS-DA: Observation definitely absent

    Given a piece of radiology text input in the format:

    <INPUT>
    <text>
    </INPUT>

    reply with the following structure:

    <OUTPUT>
    ANSWER: tuples separated by newlines. Each tuple has the format: (<clinical term text>, <label: observation-present |observation-absent|observation-uncertain|anatomy-present>). If there are no extraction related to findings or impression, return ()
    </OUTPUT>
    '''

# Create a session object for reuse
session = requests.Session()

def get_question_prompt(text):
    return f'''<INPUT>
        {text}
        </INPUT> 

        What are the clinical terms and their labels in this text? Discard sections other than FINDINGS and IMPRESSION: eg. INDICATION, HISTORY, TECHNIQUE, COMPARISON sections. If there is no extraction from findings and impression, return (). Please only output the tuples without additional notes or explanations.

        <OUTPUT> ANSWER:
        '''

def extract_entities(text, num_shots=5):
    try:
        url = 'http://ollama.corinth.informatik.rwth-aachen.de/api/chat'
        
        messages = [{'role': 'system', 'content': system_prompt}]
        messages = create_messages_with_shots(num_shots, messages)
        messages.append({'role': 'user', 'content': get_question_prompt(text)})

        data = {
            "model": "llama3.1:8b",
            "messages": messages,
            "stream": False
        }

        response = session.post(url, json=data)
        response.raise_for_status()  # 检查HTTP错误
        entities = response.json()['message']['content']

        # Parse response into JSON format
        result = {}
        lines = entities.split('\n')
        for i, line in enumerate(lines):
            if '(' in line and ')' in line:
                try:
                    term, label = eval(line.strip())
                    result[str(i+1)] = {
                        "tokens": term, 
                        "label": label
                    }
                except (ValueError, SyntaxError):
                    continue
        
        return result
        
    except Exception as e:
        print(f"Error in extract_entities: {str(e)}")
        return {}


def create_messages_with_shots(num_shots, messages):
    """
    从train.json创建few-shot示例消息列表
    
    Args:
        num_shots (int): 需要的few-shot示例数量
        messages (list): 现有的消息列表
        
    Returns:
        list: 包含few-shot示例的消息列表
    """
    # 加载训练数据
    with open('/home/hbchen/Projects/MedKGC/resource/radgraph/train.json', 'r') as f:
        train_data = json.load(f)
    
    # 获取前num_shots个示例
    shot_count = 0
    for key, value in train_data.items():
        if shot_count >= num_shots:
            break
            
        text = value['text']
        entities = value['entities']
        
        # 构建答案字符串
        answer_parts = []
        for entity_id, entity_info in entities.items():
            tokens = entity_info['tokens']
            label = entity_info['label']
            answer_parts.append(f"('{tokens}', '{label}')")
        
        answer = '\n'.join(answer_parts)
        answer += '\n</OUTPUT>'

        # 添加用户问题
        messages.append({
            'role': 'user',
            'content': get_question_prompt(text)
        })
        
        # 添加助手回答
        messages.append({
            'role': 'assistant',
            'content': answer
        })
        
        shot_count += 1
    
    return messages


def main():
    # Load test data
    with open('/home/hbchen/Projects/MedKGC/resource/radgraph/train.json', 'r') as f:
        data = json.load(f)

    # Get first example
    for key, value in data.items():
        text = value['text']
        # break
        entities = extract_entities(text, num_shots=50)  # 移除未使用的shots_path参数，添加num_shots参数
        

if __name__ == '__main__':
    main()
