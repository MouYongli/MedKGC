# from transformers import AutoTokenizer
# from transformers import AutoModelForSequenceClassification

# model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
# pt_model = AutoModelForSequenceClassification.from_pretrained(model_name)

from transformers import AutoTokenizer

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)