import requests
import Levenshtein
from openai import OpenAI
import json
import os

# Constants
API_KEY = "751b12fd-192a-4a6d-985d-9b094c99d3c8"
BASE_URL = "https://uts-ws.nlm.nih.gov/rest"


# entity as input, return json
def use_umls_api_term(entity, version="current"):

    url = f"{BASE_URL}/search/{version}"

    params = {
        "string": entity,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Query failed: {entity}, Status code: {response.status_code}")
        return None

# url as input
def use_umls_api_url(url):

    params = {
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Query failed: {url}, Status code: {response.status_code}")
        return None

# entity as input, return (id, term)
def umls_find_term(entity):

    response = use_umls_api_term(entity)

    if response and response["result"]['results']:
        results_list = response["result"]['results']

        best_match = best_match_levenshtein(entity, results_list)

        if best_match:
            return best_match["ui"], best_match["name"]

    print(f"Query umls_find_term failed: {url}, Status code: {response.status_code}")
    return None, None
            
# TODO: for further development
def best_match_levenshtein(entity, results_list):
    # for now just return the first result
    result = results_list[0]

    threshold = 3

    for result in results_list:
        distance = Levenshtein.distance(entity, result['name']) # Levenshtein NameError: name 'Levenshtein' is not defined
        if distance < threshold:
            return result
    
    return None


# id as input, return semanticTypes
def umls_id2semantic(id, version="current"):
    url = f"{BASE_URL}/content/{version}/CUI/{id}"

    params = {
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response = response.json()

        return response["result"]["semanticTypes"][0]["name"]
    else:
        print(f"Query umls_id2semantic failed: {id}, Status code: {response.status_code}")
        
        return None

# id as input, return (definition, rootSource)
def umls_id2definition(id, version="current"):
    url = f"{BASE_URL}/content/{version}/CUI/{id}/definitions"

    params = {
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response = response.json()

        if response and "result" in response:
            results_list = response["result"]

            if results_list:

                # TODO: choose the first definition
                best_match = results_list[0]

                return best_match["value"], best_match["rootSource"]
            else:
                return None, None

    else:
        print(f"Query umls_id2definition failed: {id}, Status code: {response.status_code}")
        return None, None

def normalize_entity_gpt(entity, results, myModel = "gpt-4"):
    # Initialize the OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # Convert results to a string format that can be easily parsed by the model
    results_str = json.dumps(results, indent=2)

    # Prepare the messages for the API call
    messages = [
        {"role": "system", "content": "You are an expert in named entity normalization for medical terms using the UMLS ontology. Your task is to analyze the given entity and search results, then select the most appropriate normalized form or the most likely UMLS concept."},
        {"role": "user", "content": f"Entity: {entity}\n\nSearch Results:\n{results_str}\n\nBased on these results, provide the most appropriate UI and name for this entity. If the entity is unlikely to be normalized, return ('unnormalizable', 'unnormalizable'). Respond in the format: (ui, name)"}
    ]

    # Make the API call
    completion = client.chat.completions.create(
        model = myModel,
        messages=messages
    )

    # Extract and process the response
    response = completion.choices[0].message.content.strip()

    try:
        ui, name = eval(response)
    except:
        ui, name = None, None

    return ui, name


# return metadata of the entity
def nomralize_entity_with_umls(entity):

    ui, term = umls_find_term(entity)

    if ui == None or ui == 'unnormalizable':
        return None, None, None, None, None, None
        
    semanticTypes = umls_id2semantic(ui)
    definition, source = umls_id2definition(ui)
    
    return entity, ui, term, semanticTypes, definition, source


def nomralize_entity_with_umls_and_gpt(entity):
    response = use_umls_api_term(entity)
    result_list = response['result']['results'][:5]

    ui, term = normalize_entity_gpt(entity, result_list)

    if ui == None:
        return None, None, None, None, None, None

    semanticTypes = umls_id2semantic(ui)
    definition, source = umls_id2definition(ui)
    
    return entity, ui, term, semanticTypes, definition, source