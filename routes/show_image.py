import os
from flask import Blueprint, send_from_directory
from config import IMAGE_SAVE_DIRECTORY

# Flask Blueprint for serving captured images
image_bp = Blueprint('image_bp', __name__)
"""
Blueprint: image_bp

Handles serving image files from the static directory.
Useful for displaying or accessing captured images via URL.
"""

@image_bp.route('/' + IMAGE_SAVE_DIRECTORY + '/<path:filename>')
def serve_captured_image(filename):
    """
    Serves a captured image file from the static directory.

    URL Pattern:
        /captured_images/<filename>

    Args:
        filename (str): Name of the image file to serve

    Returns:
        Response: Sends the image file from 'static/captured_images' without forcing download

    Notes:
        - Files are served from: static/<IMAGE_SAVE_DIRECTORY>
        - `as_attachment=False` allows direct display in browser
    """
    upload_folder = os.path.join('static', IMAGE_SAVE_DIRECTORY)
    return send_from_directory(upload_folder, filename, as_attachment=False)