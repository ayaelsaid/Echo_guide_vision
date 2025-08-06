import os
from config import IMAGE_SAVE_DIRECTORY, IMAGE_FILENAME

def save_pil_image_to_disk(pil_img, save_directory=IMAGE_SAVE_DIRECTORY, filename=IMAGE_FILENAME):
    """
    Saves a PIL Image object to disk at the specified directory and filename.

    This function:
    - Creates the target directory if it doesn't exist
    - Saves the image using the provided filename
    - Replaces any existing file with the same name
    - Returns the full path to the saved image

    Args:
        pil_img (PIL.Image.Image): The PIL image object to save.
        save_directory (str, optional): Directory where the image will be saved.
                                        Defaults to IMAGE_SAVE_DIRECTORY from config.
        filename (str, optional): Name of the image file (e.g., "output.png").
                                  Defaults to IMAGE_FILENAME from config.

    Returns:
        str or None: Full path to the saved image if successful, otherwise None.

    Side Effects:
        - Creates directory if missing
        - Overwrites existing image file with the same name
        - Prints status messages to stdout

    Example:
        from PIL import Image
        img = Image.new("RGB", (100, 100), color="red")
        path = save_pil_image_to_disk(img, "images", "red_square.png")
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