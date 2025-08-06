import os
import zipfile
import shutil
import wget

def download_and_extract(url, save_path_for_zip, extract_to_dir):
    """
    Downloads a ZIP file from a given URL and extracts its contents to a target directory.

    This function:
    - Creates necessary directories if they don't exist
    - Skips download and extraction if the target directory already contains files
    - Downloads the ZIP file using `wget` if not already present
    - Extracts the ZIP contents to the specified directory
    - Handles nested folders by flattening the structure (moves inner contents up)

    Args:
        url (str): The URL to download the ZIP file from.
        save_path_for_zip (str): Full path where the ZIP file should be saved.
        extract_to_dir (str): Directory where the contents should be extracted.

    Returns:
        bool: True if extraction is successful or already completed.

    Side Effects:
        - Creates directories
        - Downloads file from the internet
        - Extracts ZIP contents
        - Moves files if nested folder is detected

    Example:
        download_and_extract(
            url="https://example.com/model.zip",
            save_path_for_zip="models/vosk_model.zip",
            extract_to_dir="models/vosk_model"
        )
    """
    print("📥 Downloading model...")

    os.makedirs(os.path.dirname(save_path_for_zip), exist_ok=True)
    os.makedirs(extract_to_dir, exist_ok=True)

    # Check if already extracted
    if os.path.exists(extract_to_dir) and len(os.listdir(extract_to_dir)) > 0:
        print(f"📁 Directory '{extract_to_dir}' already exists and is not empty. Skipping download and extraction.")
        return True

    # Download if zip not present
    if not os.path.exists(save_path_for_zip):
        wget.download(url, save_path_for_zip)
        print("\n✅ Download complete!")

    print("📦 Extracting model...")
    with zipfile.ZipFile(save_path_for_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)

    # Handle nested folder if present
    subdirs = os.listdir(extract_to_dir)
    if len(subdirs) == 1:
        inner_path = os.path.join(extract_to_dir, subdirs[0])
        if os.path.isdir(inner_path):
            for item in os.listdir(inner_path):
                shutil.move(os.path.join(inner_path, item), extract_to_dir)
            os.rmdir(inner_path)

    print("✅ Extraction complete.")
    return True