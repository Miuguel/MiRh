import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import factorized

def adi_heat_simulation(matrix, num_iterations, dt, dx=1, dy=1, sigma=1):
    """
    Simula a propagação de calor usando o método ADI.
    
    :param matrix: Matriz 2D de temperatura inicial (normalizada entre 0 e 1).
    :param num_iterations: Quantas iterações devem ser feitas.
    :param dt: Passo de tempo da simulação.
    :param dx: Resolução espacial no eixo x.
    :param dy: Resolução espacial no eixo y.
    :param sigma: Coeficiente de difusão térmica.
    :return: Matriz 2D de temperatura final.
    """
    # Certificar que a matriz está normalizada
    matrix = np.clip(matrix, 0, 1)

    ny, nx = matrix.shape

    # Cálculo dos coeficientes alpha_x e alpha_y
    alpha_x = sigma * dt / (dx**2)
    alpha_y = sigma * dt / (dy**2)

    # Construir matrizes tridiagonais
    def construir_matriz_tridiagonal(n, alpha):
        diagonals = [
            -alpha * np.ones(n - 1),   # Diagonal inferior
            (1 + 2 * alpha) * np.ones(n),  # Diagonal principal
            -alpha * np.ones(n - 1)    # Diagonal superior
        ]
        return diags(diagonals, offsets=[-1, 0, 1], format='csr')

    # Criar matrizes tridiagonais para x e y
    A_x = construir_matriz_tridiagonal(nx, alpha_x).tocsc()
    A_y = construir_matriz_tridiagonal(ny, alpha_y).tocsc()


    # Pré-fatoração das matrizes para resolver rapidamente os sistemas lineares
    solver_x = factorized(A_x)
    solver_y = factorized(A_y)

    # Copiar a matriz inicial para a simulação
    U = matrix.copy()

    # Iterações no tempo
    for _ in range(num_iterations):
        # Resolver ao longo do eixo x (linhas)
        U = np.apply_along_axis(solver_x, axis=1, arr=U)

        # Resolver ao longo do eixo y (colunas)
        U = np.apply_along_axis(solver_y, axis=0, arr=U)

    return U
