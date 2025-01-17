import os
from PIL import Image

def reduce_images_in_folder(input_folder, output_folder, resolution=(800, 800), quality=50):
    """
    Reduces the resolution and quality of all images in a folder.

    Parameters:
        input_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder to save the reduced images.
        resolution (tuple): The desired resolution as (width, height).
        quality (int): Quality percentage (1-100).

    Returns:
        None
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each file in the input folder
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        # Check if the file is an image
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            try:
                with Image.open(input_path) as img:
                    # Resize the image
                    img_resized = img.resize(resolution, Image.Resampling.LANCZOS)
                    
                    # Save the reduced image to the output folder
                    output_path = os.path.join(output_folder, file_name)
                    img_resized.save(output_path, quality=quality)
                    
                    print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Example usage
input_folder = "input"    # Folder containing input images
output_folder = "output"  # Folder to save reduced images

# Reduce resolution to 800x800 and quality to 50%
reduce_images_in_folder(input_folder, output_folder, resolution=(480, 360), quality=50)
