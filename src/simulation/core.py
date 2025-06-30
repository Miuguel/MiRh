from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, Optional

class HeatSimulation(ABC):
    """Base class for heat simulation methods."""
    
    def __init__(self, dt: float, dx: float = 1.0, dy: float = 1.0, alpha: float = 1.0):
        """
        Initialize the heat simulation parameters.
        
        Args:
            dt: Time step
            dx: Spatial step in x direction
            dy: Spatial step in y direction
            alpha: Thermal diffusivity coefficient
        """
        self.dt = dt
        self.dx = dx
        self.dy = dy
        self.alpha = alpha
        self._validate_parameters()
    
    def _validate_parameters(self) -> None:
        """Validate simulation parameters."""
        if self.dt <= 0 or self.dx <= 0 or self.dy <= 0 or self.alpha <= 0:
            raise ValueError("All parameters must be positive")
    
    def _validate_input_matrix(self, matrix: np.ndarray) -> None:
        """Validate input matrix."""
        if not isinstance(matrix, np.ndarray) or matrix.ndim != 2:
            raise ValueError("Input must be a 2D numpy array")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("Input matrix contains invalid values")
    
    def _normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Normalize matrix values to [0, 1] range."""
        return np.clip(matrix, 0, 1)
    
    @abstractmethod
    def simulate(self, matrix: np.ndarray, num_iterations: int) -> np.ndarray:
        """
        Run the heat simulation.
        
        Args:
            matrix: Initial temperature matrix (2D numpy array)
            num_iterations: Number of simulation iterations
            
        Returns:
            Final temperature matrix
        """
        pass

def create_kernel(sigma_x: float, sigma_y: float) -> np.ndarray:
    """
    Create the standard heat equation kernel.
    
    Args:
        sigma_x: Diffusion coefficient in x direction
        sigma_y: Diffusion coefficient in y direction
        
    Returns:
        3x3 kernel for heat equation
    """
    sigma = sigma_x + sigma_y
    return np.array([
        [0, sigma_y, 0],
        [sigma_x, -2 * sigma, sigma_x],
        [0, sigma_y, 0]
    ])

def calculate_diffusion_coefficients(dt: float, dx: float, dy: float, alpha: float) -> Tuple[float, float]:
    """
    Calculate diffusion coefficients for the heat equation.
    
    Args:
        dt: Time step
        dx: Spatial step in x direction
        dy: Spatial step in y direction
        alpha: Thermal diffusivity coefficient
        
    Returns:
        Tuple of (sigma_x, sigma_y) diffusion coefficients
    """
    return alpha * dt / dx**2, alpha * dt / dy**2

def calculate_stability_criterion(dt: float, dx: float, dy: float, alpha: float) -> float:
    """
    Calculate the stability criterion for explicit finite difference methods.
    The simulation is stable if this value is <= 0.5.
    
    Args:
        dt: Time step
        dx: Spatial step in x direction
        dy: Spatial step in y direction
        alpha: Thermal diffusivity coefficient
        
    Returns:
        Stability criterion value
    """
    return dt * alpha * (1/dx**2 + 1/dy**2)

def calculate_total_heat(matrix: np.ndarray) -> float:
    """
    Calculate the total heat in the system (sum of all temperatures).
    This is useful for conservation checks.
    
    Args:
        matrix: Temperature matrix
        
    Returns:
        Total heat in the system
    """
    return np.sum(matrix)

def calculate_heat_flux(matrix: np.ndarray, dx: float, dy: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate the heat flux components using central differences.
    
    Args:
        matrix: Temperature matrix
        dx: Spatial step in x direction
        dy: Spatial step in y direction
        
    Returns:
        Tuple of (flux_x, flux_y) matrices
    """
    flux_x = np.zeros_like(matrix)
    flux_y = np.zeros_like(matrix)
    
    # Calculate x-component of flux (central difference)
    flux_x[:, 1:-1] = -(matrix[:, 2:] - matrix[:, :-2]) / (2 * dx)
    
    # Calculate y-component of flux (central difference)
    flux_y[1:-1, :] = -(matrix[2:, :] - matrix[:-2, :]) / (2 * dy)
    
    return flux_x, flux_y 