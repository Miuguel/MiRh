import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

def convert_to_blue_monochrome(image_path: str, output_path: str):
    """
    Convert a grayscale image to a monochromatic blue image.
    
    Args:
        image_path: Path to input grayscale image
        output_path: Path to save the blue monochrome image
    """
    # Load image and convert to grayscale if it isn't already
    img = Image.open(image_path).convert('L')
    gray_array = np.array(img, dtype=np.float64) / 255.0
    
    # Create RGB array with blue channel
    blue_array = np.zeros((*gray_array.shape, 3))
    blue_array[..., 2] = gray_array  # Set blue channel (index 2)
    
    # Convert to uint8 and save
    blue_img = Image.fromarray((blue_array * 255).astype(np.uint8))
    blue_img.save(output_path)
    
    # Display both images
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(gray_array, cmap='gray')
    ax1.set_title('Original Grayscale')
    ax1.axis('off')
    
    ax2.imshow(blue_array)
    ax2.set_title('Blue Monochrome')
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Use the example image with proper path handling
    base_dir = Path(__file__).parent.parent.parent
    input_path = base_dir / "examples" / "cameraman.jpg"
    output_path = base_dir / "examples" / "blue_cameraman.jpg"
    
    convert_to_blue_monochrome(str(input_path), str(output_path))
    print(f"Converted image saved to {output_path}") 