import json
import requests
import pprint 
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from collections import namedtuple


# Load environment variables from .env file
load_dotenv()

# Prepare prompt with instructions
system_prompt = '''
    You are a radiologist performing clinical term extraction from the FINDINGS, PA AND LATERAL CHEST RADIOGRAPH and IMPRESSION sections in the radiology report. Here a clinical term can be either anatomy or observation that is related to a finding or an impression. The anatomy term refers to an anatomical body part such as a 'lung'. The observation terms refer to observations made when referring to the associated radiology image. Observations are associated with visual features, identifiable pathophysiologic processes, or diagnostic disease classifications. For example, an observation could be 'effusion' or description phrases like 'increased'. You also need to assign a label to indicate whether the clinical term is present, absent or uncertain. 

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

        What are the clinical terms and their labels in this text? Discard sections other than FINDINGS, PA AND LATERAL CHEST RADIOGRAPH and IMPRESSION: eg. INDICATION, HISTORY, TECHNIQUE, COMPARISON sections. If there is no extraction from findings and impression, return (). Please only output the tuples without additional notes or explanations.

        <OUTPUT> ANSWER:
        '''

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
    with open('data/radgraph/original/train.json', 'r') as f:
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
    
    # print(messages)

    return messages

def parse_response(entities):
    """
    解析API响应并将其转换为JSON格式
    
    Args:
        entities (str): API响应的实体字符串
        
    Returns:
        dict: 解析后的实体字典
    """
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
    
    if not result:
        print(f'未能提取到任何实体')
        raise ValueError("未能提取到任何实体")
    else:
        print(f'提取到{len(result)}个实体')

    return result


def call_ollama_api(text, num_shots):
    model = "llama3.1:70b"

    messages = [{'role': 'system', 'content': system_prompt}]
    messages = create_messages_with_shots(num_shots, messages)
    messages.append({'role': 'user', 'content': get_question_prompt(text)})

    data = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    response = session.post(os.getenv('OLLAMA_API_URL'), json=data)
    response.raise_for_status()  # 检查HTTP错误
    
    if response.status_code == 200:
        print(f"API调用成功，状态码: {response.status_code}")
        return response.json()['message']['content']
    else:
        raise Exception(f"API调用失败，状态码: {response.status_code}")

def call_azure_openai_api(text, num_shots):
    model = "gpt-4o"

    client = AzureOpenAI(
        api_key=os.environ["AZURE_GPT_API_KEY"],  
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT")
    )

    messages = [{'role': 'system', 'content': system_prompt}]
    messages = create_messages_with_shots(num_shots, messages)
    messages.append({'role': 'user', 'content': get_question_prompt(text)})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

def extract_entities(text, num_shots=5, model='llama'):
    try:
        if model == 'llama':
            entities = call_ollama_api(text, num_shots)
        elif model == 'gpt4o':
            entities = call_azure_openai_api(text, num_shots)
        else:
            raise ValueError("Unsupported model type")

        print(entities)

        return parse_response(entities)
    except Exception as e:
        raise e

Entity = namedtuple("Entity", "e_type start_offset end_offset")

def entities_from_llm_response(json_result, text) -> list:
    entities = []
    words = text.split()
    word_index = 0
    
    for key, value in json_result.items():
        token = value['tokens']
        e_type = value['label']

        # Find the start and end word offsets of the token in the text
        while word_index < len(words):
            if words[word_index] == token:
                start_offset = word_index
                end_offset = word_index

                entities.append(Entity(e_type=e_type, start_offset=start_offset, 
                end_offset=end_offset))
                
                word_index += 1
                break
            word_index += 1
    
    return entities

if __name__ == '__main__':
    # text = "FINAL REPORT INDICATION : ___ - year - old man with change in mental status . COMPARISON : PA and lateral chest radiograph , ___ . PA AND LATERAL CHEST RADIOGRAPH : The cardiac , mediastinal and hilar contours are normal . An opacity projecting over the right mid to upper lung on the frontal view may represent focal consolidation , unchanged from ___ . Interposition of bowel accounts for the lucency below the right hemidiaphragm ."
    text = "FINAL REPORT INDICATION : ___ - year - old male with MS and hypotension . COMPARISON : ___ . TECHNIQUE : Single frontal chest radiograph was obtained portably with the patient in a semi - erect position . FINDINGS : There are low lung volumes . No focal consolidation is appreciated on this limited view . A small left pleural effusion would be difficult to exclude . Compared to prior exam , there is decreased prominence of the pulmonary vasculature . There has been interval removal of a left - sided PICC . Exam is otherwise unchanged . Slightly prominent loops of air - filled colon are again noted under the right hemidiaphragm ."
    # text = "FINAL REPORT HISTORY : Fever , to assess for pneumonia . FINDINGS : In comparison with the study of ___ , there is little change and no evidence of acute cardiopulmonary disease . The patient has taken a better inspiration and there is no pneumonia , vascular congestion or pleural effusion . The left central catheter has been removed and the Port - A - Cath tip again lies in the lower portion of the SVC ."

    # chexpert 29
    # text = "narrative : chest 2 views : 02/03 / 2007 history : male , 45 years old , post transplant . comparison : 09/18 / 06 and prior impression : unchanged right tunneled central venous catheter with tip overlying the cavoatrial junction . normal heart size and pulmonary vascularity . no focal consolidation , pleural effusion , or pneumothorax . bones are unremarkable . summary : 2 - abnormal , previously reported accession number : 645666774 this report has been anonymized . all dates are offset from the actual dates by a fixed interval associated with the patient ."
    
    entities = extract_entities(text, num_shots=10)
    # entities = extract_entities(text, num_shots=100, model='azure_openai')  


    print(entities)
