import os
import numpy as np
from PIL import Image

def save_images_in_formats(input_path, output_folder, formats, file_identifier):
    os.makedirs(output_folder, exist_ok=True)
    saved_paths = []
    
    for fmt in formats:
        output_path = os.path.join(output_folder, f"{file_identifier}.{fmt.lower()}")
        img = Image.open(input_path)
        img.save(output_path, format=fmt)
        saved_paths.append(output_path)
    
    return saved_paths

def compare_images_pixelwise(img1_path, img2_path):
    try:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        if arr1.shape != arr2.shape:
            return False
        
        return np.array_equal(arr1, arr2)
    except Exception as e:
        print(f"Error comparing images: {e}")
        return False

def compare_all_conversions(input_paths, output_folder, formats):
    results = {}
    
    for i, input_path in enumerate(input_paths, 1):
        if not os.path.exists(input_path):
            print(f"Warning: Input file {input_path} doesn't exist")
            continue
            
        file_id = f"5.3.{i}"
        converted_paths = save_images_in_formats(input_path, output_folder, formats, file_id)
        
        comparisons = []
        for conv_path in converted_paths:
            comparisons.append({
                'converted_path': conv_path,
                'is_identical': compare_images_pixelwise(input_path, conv_path)
            })
        
        results[input_path] = comparisons
    
    return results

def print_comparison_results(results):
    for original_path, comparisons in results.items():
        print(f"\nComparison results for {original_path}:")
        
        for comp in comparisons:
            status = "IDENTICAL" if comp['is_identical'] else "DIFFERENT"
            print(f"{status}: {original_path} vs {comp['converted_path']}")

def main():
    input_image_paths = ["5.3.1.jpg", "5.3.2.jpg", "5.3.3.jpg"]
    output_folder = "output"
    formats = ['JPEG', 'TIFF', 'PNG', 'BMP']
    
    results = compare_all_conversions(input_image_paths, output_folder, formats)
    print_comparison_results(results)

if __name__ == "__main__":
    main()