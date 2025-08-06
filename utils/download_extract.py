import os
import zipfile
import shutil
import wget

def download_and_extract(url, save_path_for_zip, extract_to_dir):
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