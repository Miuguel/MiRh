import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Tuple
from .core import (
    HeatSimulation, create_kernel, calculate_diffusion_coefficients,
    calculate_total_heat, calculate_heat_flux
)

class FFTHeatSimulation(HeatSimulation):
    """Heat simulation using FFT-based convolution."""
    
    def __init__(self, dt: float, dx: float = 1.0, dy: float = 1.0, alpha: float = 1.0):
        super().__init__(dt, dx, dy, alpha)
        self._kernel_fft = None
        self._kernel_shape = None
        self._initial_heat = None
    
    def _compute_kernel_fft(self, matrix_shape: Tuple[int, int]) -> None:
        """
        Compute and cache the FFT of the kernel for the given matrix shape.
        
        Args:
            matrix_shape: Shape of the input matrix (height, width)
        """
        if self._kernel_shape == matrix_shape:
            return
            
        # Calculate diffusion coefficients using utility function
        sigma_x, sigma_y = calculate_diffusion_coefficients(
            self.dt, self.dx, self.dy, self.alpha
        )
        
        # Create kernel
        kernel = create_kernel(sigma_x, sigma_y)
        
        # Pad kernel to optimal size for FFT
        padded_shape = self._get_optimal_fft_shape(matrix_shape)
        kernel_padded = np.zeros(padded_shape)
        kh, kw = kernel.shape
        
        # Place kernel in center of padded array
        center_y = padded_shape[0] // 2 - kh // 2
        center_x = padded_shape[1] // 2 - kw // 2
        kernel_padded[center_y:center_y + kh, center_x:center_x + kw] = kernel
        
        # Normalize kernel to preserve heat
        kernel_padded = kernel_padded / np.sum(kernel_padded)
        
        # Compute FFT
        self._kernel_fft = fft2(kernel_padded)
        self._kernel_shape = matrix_shape
    
    def _get_optimal_fft_shape(self, matrix_shape: Tuple[int, int]) -> Tuple[int, int]:
        """
        Get optimal shape for FFT computation.
        Uses next power of 2 for better FFT performance.
        """
        def next_power_of_2(n: int) -> int:
            return 1 << (n - 1).bit_length()
        
        return (next_power_of_2(matrix_shape[0]), next_power_of_2(matrix_shape[1]))
    
    def _pad_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Pad matrix to optimal FFT size with Neumann boundary conditions."""
        padded_shape = self._get_optimal_fft_shape(matrix.shape)
        padded = np.zeros(padded_shape)
        
        # Copy original matrix to center
        center_y = padded_shape[0] // 2 - matrix.shape[0] // 2
        center_x = padded_shape[1] // 2 - matrix.shape[1] // 2
        padded[center_y:center_y + matrix.shape[0], center_x:center_x + matrix.shape[1]] = matrix
        
        # Apply Neumann boundary conditions to padded regions
        padded[:center_y, :] = padded[center_y:center_y+1, :]  # Top
        padded[center_y + matrix.shape[0]:, :] = padded[center_y + matrix.shape[0]-1:center_y + matrix.shape[0], :]  # Bottom
        padded[:, :center_x] = padded[:, center_x:center_x+1]  # Left
        padded[:, center_x + matrix.shape[1]:] = padded[:, center_x + matrix.shape[1]-1:center_x + matrix.shape[1]]  # Right
        
        return padded
    
    def _unpad_matrix(self, padded_matrix: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
        """Remove padding from matrix."""
        return padded_matrix[:original_shape[0], :original_shape[1]]
    
    def simulate(self, matrix: np.ndarray, num_iterations: int) -> np.ndarray:
        """
        Run the heat simulation using FFT-based convolution.
        
        Args:
            matrix: Initial temperature matrix (2D numpy array)
            num_iterations: Number of simulation iterations
            
        Returns:
            Final temperature matrix
        """
        self._validate_input_matrix(matrix)
        matrix = self._normalize_matrix(matrix)
        
        # Store initial heat for conservation check
        self._initial_heat = calculate_total_heat(matrix)
        
        # Compute and cache kernel FFT
        self._compute_kernel_fft(matrix.shape)
        
        # Pad matrix for FFT
        padded_matrix = self._pad_matrix(matrix)
        matrix_fft = fft2(padded_matrix)
        
        # Apply kernel in frequency domain
        for _ in range(num_iterations):
            matrix_fft = matrix_fft * (1 + self._kernel_fft)  # Use multiplication for stability
        
        # Transform back to spatial domain and unpad
        result = np.real(ifft2(matrix_fft))
        result = self._unpad_matrix(result, matrix.shape)
        
        # Normalize and verify heat conservation
        result = self._normalize_matrix(result)
        final_heat = calculate_total_heat(result)
        if not np.isclose(self._initial_heat, final_heat, rtol=1e-5):
            print(f"Warning: Heat conservation violated. Initial: {self._initial_heat:.3f}, Final: {final_heat:.3f}")
        
        return result 