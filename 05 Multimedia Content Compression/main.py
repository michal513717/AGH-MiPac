from PIL import Image
import os

def save_images_in_formats(input_paths, output_folder):
    formats = ['JPEG', 'TIFF', 'PNG', 'BMP']
    os.makedirs(output_folder, exist_ok=True)
    
    for i, input_path in enumerate(input_paths):
        img = Image.open(input_path)
        for fmt in formats:
            output_path = os.path.join(output_folder, f"image_{i+1}.{fmt.lower()}")
            img.save(output_path, format=fmt)

input_image_paths = ["5.3.1.jpg", "5.3.2.jpg", "5.3.3.jpg"]
output_folder = "examples"
save_images_in_formats(input_image_paths, output_folder)
