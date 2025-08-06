from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

def init_ai(image_pil, text):
    model_id = "D:/Echoguid_vision/gemma-3n-transformers-gemma-3n-e2b-v2"
    processor = AutoProcessor.from_pretrained(model_id)

    model = AutoModelForImageTextToText.from_pretrained(model_id)
    
    prompt = f"<image_soft_token> {text}"

    model_inputs = processor(text=prompt, images=image_pil, return_tensors="pt").to(model.device)

    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**model_inputs, max_new_tokens=10)
        generation = generation[0][input_len:]

    decoded = processor.decode(generation, skip_special_tokens=True)
    return decoded