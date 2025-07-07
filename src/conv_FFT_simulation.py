import numpy as np
from scipy.fft import fft2, ifft2, fftshift

def conv_simulation_fft(matrix, num_iterations, dt, dx=1, dy=1, alpha=1):
    """
    Executa a simulação de calor usando FFT para otimizar a convolução.
    
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

    # Expandir o kernel para o tamanho da matriz de entrada com zero-padding
    kernel_padded = np.zeros_like(matrix)
    kh, kw = kernel.shape
    kernel_padded[:kh, :kw] = kernel

    # Centralizar o kernel para evitar deslocamentos na convolução via FFT
    kernel_padded = fftshift(kernel_padded)

    # Transformada de Fourier do kernel e da matriz de entrada
    kernel_fft = fft2(kernel_padded)
    U_fft = fft2(matrix)

    # Iterações da simulação
    for _ in range(num_iterations):
        U_fft += kernel_fft * U_fft  # Multiplicação no domínio da frequência
    
    # Transformada inversa para voltar ao domínio espacial
    U = np.real(ifft2(U_fft))

    # Normalizar novamente a matriz
    U = np.clip(U, 0, 1)

    return U
