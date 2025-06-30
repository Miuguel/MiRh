from typing import Tuple, List
import numpy as np
from PIL import Image
from pathlib import Path

class ImageProcessor:
    """Handles image loading, processing, and saving operations."""
    
    @staticmethod
    def load_image(image_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load an image and return its RGB channels as separate numpy arrays.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (R, G, B) channels as numpy arrays
        """
        image = Image.open(image_path).convert('RGB')
        image_array = np.array(image)
        return (
            image_array[:, :, 0].astype(float) / 255,  # R channel
            image_array[:, :, 1].astype(float) / 255,  # G channel
            image_array[:, :, 2].astype(float) / 255   # B channel
        )
    
    @staticmethod
    def combine_channels(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Combine RGB channels into a single image array.
        
        Args:
            r: Red channel array
            g: Green channel array
            b: Blue channel array
            
        Returns:
            Combined RGB image array
        """
        return np.stack((r, g, b), axis=-1)
    
    @staticmethod
    def save_image(image_array: np.ndarray, output_path: str) -> None:
        """
        Save an image array to a file.
        
        Args:
            image_array: RGB image array (values in [0, 1])
            output_path: Path where to save the image
        """
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to uint8 and save
        image_array = np.clip(image_array * 255, 0, 255).astype(np.uint8)
        Image.fromarray(image_array).save(output_path)
    
    @staticmethod
    def process_channels(
        channels: List[np.ndarray],
        simulation_func,
        num_iterations: List[int],
        **simulation_kwargs
    ) -> List[np.ndarray]:
        """
        Process multiple channels using a simulation function.
        
        Args:
            channels: List of channel arrays to process
            simulation_func: Function to apply to each channel
            num_iterations: List of iteration counts for each channel
            **simulation_kwargs: Additional arguments for the simulation function
            
        Returns:
            List of processed channel arrays
        """
        if len(channels) != len(num_iterations):
            raise ValueError("Number of channels must match number of iteration counts")
            
        return [
            simulation_func(channel, iterations, **simulation_kwargs)
            for channel, iterations in zip(channels, num_iterations)
        ] 