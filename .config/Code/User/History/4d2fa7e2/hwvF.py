import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    if isinstance(image_path, Image.Image):  
        image = np.array(image_path)
    else:
        image = np.array(Image.open(image_path))

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    adaptive_thresh = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    coords = np.column_stack(np.where(adaptive_thresh > 0))

    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle
    else:
        angle = 0

    (h, w) = adaptive_thresh.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    deskewed = cv2.warpAffine(
        adaptive_thresh, M, (w, h), 
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    
    return Image.fromarray(deskewed)
