import cv2
import numpy as np
from PIL import Image

def preprocess_invoice_image(image_path: str, target_size=(1024, 1024)) -> Image.Image:
    # Load image in using OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding to detect text regions
    # Pixels lighter than 180 become 0 (black)
    # Pixels darker than 180 become 255 (white)
    # Then we invert it (THRESH_BINARY_INV) so that text (dark) becomes white, and background (light) becomes black.
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Find contours to crop to only the content
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        img = img[y:y+h, x:x+w]

    
    # Resize while maintain aspect ratio
    h, w, _ = img.shape
    scale = min(target_size[0] / w, target_size[1] / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h))

    top = (target_size[1] - new_h) // 2
    bottom = target_size[1] - new_h - top
    left = (target_size[0] - new_w) // 2
    right = target_size[0] - new_w - left

    # Pad out to get to 1024x1024
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Convert back to pil image
    return Image.fromarray(cv2.cvtColor(padded, cv2.COLOR_BGR2RGB))