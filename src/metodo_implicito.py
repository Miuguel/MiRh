import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve


def construir_matriz_tridiagonal(n, sigma):
    """
    Constrói uma matriz tridiagonal esparsa para o método implícito.
    
    :param n: Número de pontos na direção (x ou y).
    :param sigma: Fator de difusão em uma direção (x ou y).
    :return: Matriz tridiagonal esparsa no formato CSR.
    """
    diagonals = [
        -sigma * np.ones(n - 1),    # Diagonal inferior
        (1 + 2 * sigma) * np.ones(n),  # Diagonal principal
        -sigma * np.ones(n - 1)     # Diagonal superior
    ]
    return diags(diagonals, offsets=[-1, 0, 1], format='csr')


def resolver_direcao_alternada(U, A, axis):
    """
    Resolve o sistema linear em uma direção (x ou y) usando o método implícito.
    
    :param U: Matriz de temperatura atual.
    :param A: Matriz tridiagonal esparsa correspondente à direção.
    :param axis: 0 para resolver ao longo de x, 1 para resolver ao longo de y.
    :return: Matriz U atualizada.
    """
    if axis == 0:  # Resolver ao longo de x (linhas)
        for j in range(U.shape[1]):
            U[:, j] = spsolve(A, U[:, j])
    elif axis == 1:  # Resolver ao longo de y (colunas)
        for i in range(U.shape[0]):
            U[i, :] = spsolve(A, U[i, :])
    return U


def metodo_implicito(U_inicial, alpha, dt, Tf, Lx, Ly):
    """
    Executa a simulação de calor usando o método implícito.
    
    :param U_inicial: Matriz 2D de temperatura inicial (normalizada entre 0 e 1).
    :param alpha: Difusividade térmica.
    :param dt: Intervalo de tempo.
    :param Tf: Tempo total de simulação.
    :param Lx: Comprimento físico na direção x.
    :param Ly: Comprimento físico na direção y.
    :return: Matriz 2D de temperatura final.
    """
    # Obter dimensões da matriz inicial
    ny, nx = U_inicial.shape

    # Calcular os deltas espaciais
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)

    # Calcular os sigmas (fatores de difusão)
    sigma_x = alpha * dt / dx**2
    sigma_y = alpha * dt / dy**2

    # Verificar condição de estabilidade
    if sigma_x + sigma_y > 0.5:
        raise ValueError("Condição de estabilidade violada! Reduza dt ou aumente dx/dy.")

    # Construir as matrizes tridiagonais
    A_x = construir_matriz_tridiagonal(nx, sigma_x)
    A_y = construir_matriz_tridiagonal(ny, sigma_y)

    # Inicializar o campo de temperatura
    U = U_inicial.copy()

    # Número de passos de tempo
    nT = int(Tf / dt)

    # Iterações no tempo
    for _ in range(nT):
        U = resolver_direcao_alternada(U, A_x, axis=0)  # Passo 1: resolver ao longo de x
        U = resolver_direcao_alternada(U, A_y, axis=1)  # Passo 2: resolver ao longo de y

    return U
