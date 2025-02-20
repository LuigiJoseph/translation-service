# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# import yaml
# from pathlib import Path
# from huggingface_hub import login

# from log.loggers import logger

# configfile_path = Path("/configs/config.yaml")
# # configfile_path = Path(__file__).resolve().parents[2] / "configs"/"config.yaml"

# try:
#     with open(configfile_path, "r") as file:
#         logger.info("File opened successfully!")

#         config = yaml.safe_load(file)
# except Exception as e:
#     print(f"Error opening file: {e}")

# #login with token in hugging face
# try:
#     hugging_token = config["huggingface"]["token"]
#     login(token=hugging_token)
# except KeyError:
#     logger.info("Token key not found in the configuration file.")
# except Exception as e:
#     print(f"Failed to log in: {e}")

# # Model name
# model_name = "Qwen/Qwen2.5-1.5B-Instruct"


# # Change this if using windows
# device = "cpu"

# logger.info(f"Using device: {device}")

# # Load model and tokenizer
# model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
# tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# def translate_text(text,source_lang,target_lang):

#     # Define prompt
#     messages = [
#         {"role": "system", "content": "You are a translator with the source and target locales of both languages. You only return the translated text."},
#         {"role": "user", "content": f"Translate from {source_lang} to {target_lang} the following text: {text}"}
#     ]

#     formatted_text = tokenizer.apply_chat_template(
#         messages,
#         tokenize=True,  
#         add_generation_prompt=True  
#     )
#     formatted_text = tokenizer.decode(formatted_text)
#     model_inputs = tokenizer([formatted_text], return_tensors="pt").to(device)

#     # Generate response
#     generated_ids = model.generate(
#         **model_inputs,
#         max_new_tokens=100,
#         pad_token_id=tokenizer.eos_token_id  
#     )

#     # Decode and print output
#     response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
#     response = response.split("assistant")[-1].strip()

    

#     return response


# #testing
# # source_lang = "English"
# # target_lang = "Turkish"
# # text_to_translate = "Hello, how are you?"
# # translated_text = translate_text(text_to_translate, source_lang, target_lang)
# # print("Translated Text:", translated_text)