from transformers import MarianMTModel, MarianTokenizer

MODEL_NAME = "ckartal/turkish-to-english-finetuned-model"
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME)

# Translation Function
def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
