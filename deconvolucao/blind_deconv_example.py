import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from deconvolution.blind_deconv import BlindDeconvolution

def load_image(image_path: str) -> np.ndarray:
    """Load and convert image to grayscale float array."""
    img = Image.open(image_path).convert('L')
    return np.array(img, dtype=np.float64) / 255.0

def save_image(image: np.ndarray, output_path: str):
    """Save image from float array."""
    img = Image.fromarray((np.clip(image, 0, 1) * 255).astype(np.uint8))
    img.save(output_path)

def plot_results(original: np.ndarray, blurred: np.ndarray, 
                restored: np.ndarray, psf: np.ndarray,
                metrics: dict):
    """Plot original, blurred, restored images and estimated PSF."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot images
    axes[0,0].imshow(original, cmap='gray')
    axes[0,0].set_title('Original Image')
    axes[0,0].axis('off')
    
    axes[0,1].imshow(blurred, cmap='gray')
    axes[0,1].set_title('Blurred Image')
    axes[0,1].axis('off')
    
    axes[1,0].imshow(restored, cmap='gray')
    axes[1,0].set_title(f'Restored Image\nPSNR: {metrics["psnr"]:.2f} dB\nSSIM: {metrics["ssim"]:.3f}')
    axes[1,0].axis('off')
    
    # Plot PSF
    im = axes[1,1].imshow(psf, cmap='hot')
    axes[1,1].set_title('Estimated PSF')
    axes[1,1].axis('off')
    plt.colorbar(im, ax=axes[1,1])
    
    plt.tight_layout()
    plt.show()

def main():
    # Load image
    base_dir = Path(__file__).parent.parent.parent
    input_path = base_dir / "examples" / "cameraman.jpg"
    output_path = base_dir / "examples" / "unblurred_cameraman.jpg"
    
    # Load and normalize image
    original = load_image(input_path)
    
    # Create synthetic blur (for demonstration)
    # In real cases, you would use an actual blurred image
    from scipy.ndimage import gaussian_filter
    blurred = gaussian_filter(original, sigma=2.0)
    
    # Initialize and run blind deconvolution
    deconv = BlindDeconvolution(max_psf_size=15, regularization=1e-6)
    result = deconv.deconvolve(blurred)
    
    # Save result
    save_image(result.restored_image, output_path)
    
    # Plot results
    metrics = {
        'psnr': result.psnr,
        'ssim': result.ssim,
        'mse': result.mse
    }
    plot_results(original, blurred, result.restored_image, 
                result.estimated_psf, metrics)
    
    print(f"Deconvolution completed. Results saved to {output_path}")
    print(f"Metrics:")
    print(f"PSNR: {metrics['psnr']:.2f} dB")
    print(f"SSIM: {metrics['ssim']:.3f}")
    print(f"MSE: {metrics['mse']:.6f}")

if __name__ == '__main__':
    main() 