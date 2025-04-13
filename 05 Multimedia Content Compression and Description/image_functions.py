import os
from PIL import Image

def save_images_in_formats(input_path, output_folder, formats, file_identifier):
    os.makedirs(output_folder, exist_ok=True)
    saved_paths = []
    
    for fmt in formats:
        output_path = os.path.join(output_folder, f"{file_identifier}_image.{fmt.lower()}")
        img = Image.open(input_path)
        img.save(output_path, format=fmt)
        saved_paths.append(output_path)
    
    return saved_paths

def main(input_image_paths, output_folder, formats):
    for i, input_image_path in enumerate(input_image_paths, start=1):
        file_identifier = f"5.3.{i}"
        save_images_in_formats(input_image_path, output_folder, formats, file_identifier)


if __name__ == "__main__":
    input_image_paths = ["5.3.1.jpg", "5.3.2.jpg", "5.3.3.jpg"]
    output_folder = "output"
    formats = ['JPEG', 'TIFF', 'PNG', 'BMP']

    main(input_image_paths, output_folder, formats)