import numpy as np
from typing import Tuple
from .core import HeatSimulation, create_kernel

class FiniteDiffHeatSimulation(HeatSimulation):
    """Heat simulation using explicit finite difference method."""
    
    def __init__(self, dt: float, dx: float = 1.0, dy: float = 1.0, alpha: float = 1.0):
        super().__init__(dt, dx, dy, alpha)
        self._check_stability()
    
    def _check_stability(self) -> None:
        """
        Check numerical stability of the simulation parameters.
        For explicit finite difference, we need: dt * alpha * (1/dx^2 + 1/dy^2) <= 0.5
        """
        stability_criterion = self.dt * self.alpha * (1/self.dx**2 + 1/self.dy**2)
        if stability_criterion > 0.5:
            raise ValueError(
                f"Simulation parameters violate stability criterion: {stability_criterion:.3f} > 0.5. "
                "Try reducing dt or increasing dx/dy."
            )
    
    def _apply_boundary_conditions(self, matrix: np.ndarray) -> np.ndarray:
        """
        Apply Neumann boundary conditions (zero flux at boundaries).
        This preserves the total heat in the system.
        """
        matrix[0, :] = matrix[1, :]  # Top boundary
        matrix[-1, :] = matrix[-2, :]  # Bottom boundary
        matrix[:, 0] = matrix[:, 1]  # Left boundary
        matrix[:, -1] = matrix[:, -2]  # Right boundary
        return matrix
    
    def simulate(self, matrix: np.ndarray, num_iterations: int) -> np.ndarray:
        """
        Run the heat simulation using explicit finite difference method.
        
        Args:
            matrix: Initial temperature matrix (2D numpy array)
            num_iterations: Number of simulation iterations
            
        Returns:
            Final temperature matrix
        """
        self._validate_input_matrix(matrix)
        matrix = self._normalize_matrix(matrix)
        
        # Calculate diffusion coefficients
        sigma_x = self.alpha * self.dt / self.dx**2
        sigma_y = self.alpha * self.dt / self.dy**2
        
        # Create kernel for finite difference stencil
        kernel = create_kernel(sigma_x, sigma_y)
        
        # Run simulation
        current = matrix.copy()
        for _ in range(num_iterations):
            # Apply convolution using the finite difference stencil
            next_state = current.copy()
            next_state[1:-1, 1:-1] += (
                sigma_x * (current[1:-1, 2:] + current[1:-1, :-2] - 2*current[1:-1, 1:-1]) +
                sigma_y * (current[2:, 1:-1] + current[:-2, 1:-1] - 2*current[1:-1, 1:-1])
            )
            
            # Apply boundary conditions
            next_state = self._apply_boundary_conditions(next_state)
            
            # Update current state
            current = next_state
        
        return self._normalize_matrix(current) 