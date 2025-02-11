from transformers import MarianMTModel, MarianTokenizer

MODELS={ 
    "tr-en": {
                    "name": "ckartal/turkish-to-english-finetuned-model",  
                    "src_lang": "tr",
                    "tgt_lang": "en",
                },
    "en-tr": {
                    "name": "ckartal/english-to-turkish-finetuned-model",
                    "src_lang": "en",
                    "tgt_lang": "tr",
                },
    "en-ar": {
                    "name": "Helsinki-NLP/opus-mt-tc-big-en-ar",
                    "src_lang": "en",
                    "tgt_lang": "ar",
                }
    }

for key, model_info in MODELS.items():
    try:
        model_info["tokenizer"] = MarianTokenizer.from_pretrained(model_info["name"])
        model_info["model"] = MarianMTModel.from_pretrained(model_info["name"])
    except Exception as e:
        print(f"Warning: Failed to load model {model_info['name']} - {str(e)}")


# gives model used 
used_models = set()

def mark_model_used(model_key):
    if model_key in MODELS:
        used_models.add(MODELS[model_key]["name"])


# Translation Function
def translate_text(text, source_target_locale):

    if source_target_locale not in MODELS:
        return "Error: Model not found"

    model_info = MODELS[source_target_locale]
    tokenizer = model_info["tokenizer"]
    model = model_info["model"]

    if not tokenizer or not model:
        return f"Error: Model {model_info['name']} failed to load"

    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    
    except Exception as e:
        return f"Translation failed: {str(e)}"
