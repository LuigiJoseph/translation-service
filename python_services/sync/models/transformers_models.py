from transformers import MarianMTModel, MarianTokenizer

from python_services.sync.log.loggers import logger
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
                },
    "ar-en": {
                    "name": "Helsinki-NLP/opus-mt-ar-en",
                    "src_lang": "ar",
                    "tgt_lang": "en",
                }
    }


#load models
for key, model_info in MODELS.items():
    try:
        model_info["tokenizer"] = MarianTokenizer.from_pretrained(model_info["name"])
        model_info["model"] = MarianMTModel.from_pretrained(model_info["name"])
    except Exception as e:
        logger.info(f"Warning: Failed to load model {model_info['name']} - {str(e)}")

# Translation Function
def translate_text(text, source, target):
    # Construct the key dynamically
    source_target_locale = f"{source}-{target}"
    
    if source_target_locale not in MODELS:
        return f"Error: No model found for {source} to {target} translation"

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
