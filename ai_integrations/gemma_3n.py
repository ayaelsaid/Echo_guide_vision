from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

def init_ai(image_pil, text):
    """
    Generates a textual response from a vision-language model using an image and a prompt.

    This function:
    - Loads a pre-trained image-text-to-text model using Transformers
    - Prepares the input by combining the image with a textual prompt
    - Performs inference using the model in no-grad mode
    - Decodes the generated output into a human-readable string

    Args:
        image_pil (PIL.Image.Image): The input image in PIL format.
        text (str): The textual prompt to guide the model's response.

    Returns:
        str: The generated textual output from the model.

    Notes:
        - Uses `AutoProcessor` and `AutoModelForImageTextToText` from Hugging Face
        - Assumes the model is stored locally at `model_id` path
        - Uses `<image_soft_token>` to indicate image embedding in prompt
        - Limits generation to `max_new_tokens=10` for brevity

    Example:
        response = init_ai(image_pil, "Describe the scene for a blind user.")
    """

    model_id = "E:\Echo_Guide_Vision\models\google\gemma-3n-transformers-gemma-3n-e2b-v2"
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