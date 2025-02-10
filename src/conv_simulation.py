import numpy as np
from scipy.ndimage import convolve

def conv_simulation(matrix, num_iterations, dt, dx=1, dy=1, alpha=1):
    """
    Executa a simulação de calor usando o método de convolução.
    
    :param matrix: Matriz 2D de temperatura inicial (normalizada entre 0 e 1).
    :param num_iterations: Quantas iterações devem ser feitas.
    :param dt: Passo de tempo da simulação.
    :param dx: Resolução espacial no eixo x.
    :param dy: Resolução espacial no eixo y.
    :param alpha: Coeficiente de difusão térmica.
    :return: Matriz 2D de temperatura final.
    """
    # Certificar que a matriz está normalizada
    matrix = np.clip(matrix, 0, 1)
    # Calcular os fatores de espalhamento 
    sigma_x = alpha * dt / dx**2
    sigma_y = alpha * dt / dy**2
    sigma = sigma_x + sigma_y 

    # Verificar estabilidade
    assert sigma <= 0.5, "Condição de estabilidade violada! Reduza dt ou aumente dx/dy."

    # Kernel para convolução
    kernel = np.array([[0, sigma_y, 0],
                       [sigma_x, -2 * sigma, sigma_x],
                       [0, sigma_y, 0]])

    # Copiar a matriz inicial para a simulação
    U = matrix.copy()

    # Iterações da simulação
    for _ in range(num_iterations):
        U += convolve(U, kernel, mode='constant', cval=0.0)

    return U
