import cv2
import numpy as np
from PIL import Image
from rembg import remove
import sys

def prep_photo(input_path, output_path="source-prepped.png"):
    # 1. Load image and remove background
    input_img = Image.open(input_path)
    output_rgba = remove(input_img)
    
    # 2. Composite onto pure white background
    white_bg = Image.new("RGBA", output_rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, output_rgba).convert("L")
    
    # 3. Apply CLAHE for high contrast shading
    img_np = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(img_np)
    
    # Save result
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped image saved to {output_path}")

if __name__ == "__main__":
    image_file = sys.argv[1] if len(sys.argv) > 1 else "image_81bf0b.jpg"
    prep_photo(image_file)