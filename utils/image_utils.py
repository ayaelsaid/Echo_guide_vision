import os
import PIL.Image
from config import IMAGE_SAVE_DIRECTORY, IMAGE_FILENAME

def save_pil_image_to_disk(pil_img, save_directory=IMAGE_SAVE_DIRECTORY, filename=IMAGE_FILENAME):
    """
    Saves a PIL Image to a specified directory on disk, replacing any existing file
    with the same name to save space.
    Creates the directory if it doesn't exist.
    Returns the full path to the saved image.
    """
    if pil_img is None:
        print("No PIL image provided to save.")
        return None

    os.makedirs(save_directory, exist_ok=True)

    full_path = os.path.join(save_directory, filename)

    try:
        pil_img.save(full_path)
        print(f"Image saved successfully and replaced existing at: {full_path}")
        return full_path
    except Exception as e:
        print(f"Error saving image to disk: {e}")
        return None