import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import factorized
from typing import Tuple
from .core import HeatSimulation, calculate_total_heat

class ADIHeatSimulation(HeatSimulation):
    """Heat simulation using Alternating Direction Implicit (ADI) method."""
    
    def __init__(self, dt: float, dx: float = 1.0, dy: float = 1.0, alpha: float = 1.0):
        super().__init__(dt, dx, dy, alpha)
        self._solver_x = None
        self._solver_y = None
        self._matrix_shape = None
        self._initial_heat = None
    
    def _build_tridiagonal_matrix(self, n: int, alpha: float):
        """Build tridiagonal matrix for ADI method."""
        diagonals = [
            -alpha * np.ones(n - 1),   # Lower diagonal
            (1 + 2 * alpha) * np.ones(n),  # Main diagonal
            -alpha * np.ones(n - 1)    # Upper diagonal
        ]
        return diags(diagonals, offsets=[-1, 0, 1], format='csc')
    
    def _compute_solvers(self, matrix_shape: Tuple[int, int]) -> None:
        """Compute and cache the matrix solvers for the given shape."""
        if self._matrix_shape == matrix_shape:
            return
            
        # Calculate diffusion coefficients
        alpha_x = self.alpha * self.dt / (self.dx**2)
        alpha_y = self.alpha * self.dt / (self.dy**2)
        
        # Build and factorize matrices
        A_x = self._build_tridiagonal_matrix(matrix_shape[1], alpha_x)
        A_y = self._build_tridiagonal_matrix(matrix_shape[0], alpha_y)
        
        self._solver_x = factorized(A_x)
        self._solver_y = factorized(A_y)
        self._matrix_shape = matrix_shape
    
    def _apply_boundary_conditions(self, matrix: np.ndarray) -> np.ndarray:
        """Apply Neumann boundary conditions (zero flux at boundaries)."""
        matrix[0, :] = matrix[1, :]  # Top boundary
        matrix[-1, :] = matrix[-2, :]  # Bottom boundary
        matrix[:, 0] = matrix[:, 1]  # Left boundary
        matrix[:, -1] = matrix[:, -2]  # Right boundary
        return matrix
    
    def simulate(self, matrix: np.ndarray, num_iterations: int) -> np.ndarray:
        """
        Run the heat simulation using ADI method.
        
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
        
        # Compute solvers for this matrix shape
        self._compute_solvers(matrix.shape)
        
        # Run simulation
        current = matrix.copy()
        for _ in range(num_iterations):
            # Step 1: Solve along x-direction (rows)
            for i in range(current.shape[0]):
                current[i, :] = self._solver_x(current[i, :])
            
            # Apply boundary conditions after x-step
            current = self._apply_boundary_conditions(current)
            
            # Step 2: Solve along y-direction (columns)
            for j in range(current.shape[1]):
                current[:, j] = self._solver_y(current[:, j])
            
            # Apply boundary conditions after y-step
            current = self._apply_boundary_conditions(current)
        
        # Normalize and verify heat conservation
        result = self._normalize_matrix(current)
        final_heat = calculate_total_heat(result)
        if not np.isclose(self._initial_heat, final_heat, rtol=1e-5):
            print(f"Warning: Heat conservation violated. Initial: {self._initial_heat:.3f}, Final: {final_heat:.3f}")
        
        return result 