import numpy as np
from PIL import Image
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import os

# Configurações físicas e temporais
alpha = 1.0      # Difusividade térmica
dt = 0.01        # Intervalo de tempo
Tf = 1.0         # Tempo total de simulação
Ly = Lx = 1.0    # Comprimento físico do domínio (ajustável)

# Carregar a imagem e definir nx e ny
caminho_imagem = 'examples/example_image.png'
imagem = Image.open(caminho_imagem).convert('L')  # Converter para escala de cinza
imagem_array = np.array(imagem, dtype=float) / 255  # Normalizar entre 0 e 1

ny, nx = imagem_array.shape  # Dimensões da imagem
dx = Lx / (nx - 1)
dy = Ly / (ny - 1)
sigma_x = alpha * dt / dx**2
sigma_y = alpha * dt / dy**2

# Verificar estabilidade
# assert sigma_x + sigma_y <= 0.5, "Condição de estabilidade violada! Reduza dt ou aumente dx/dy."

# Construir a matriz tridiagonal para o método implícito (em x e y)
def construir_matriz_tridiagonal(n, sigma):
    diagonals = [
        -sigma * np.ones(n - 1),   # Diagonal inferior
        (1 + 2 * sigma) * np.ones(n),  # Diagonal principal
        -sigma * np.ones(n - 1)    # Diagonal superior
    ]
    return diags(diagonals, offsets=[-1, 0, 1], format='csr')

A_x = construir_matriz_tridiagonal(nx, sigma_x)  # Matriz A no eixo x
A_y = construir_matriz_tridiagonal(ny, sigma_y)  # Matriz A no eixo y

# Inicializar o campo de temperatura
U = imagem_array.copy()

# Função para resolver em uma dimensão (direção alternada)
def resolver_direcao_alternada(U, A, axis):
    if axis == 0:  # Resolver ao longo de x (linhas)
        for j in range(U.shape[1]):
            U[:, j] = spsolve(A, U[:, j])
    elif axis == 1:  # Resolver ao longo de y (colunas)
        for i in range(U.shape[0]):
            U[i, :] = spsolve(A, U[i, :])
    return U

# Iterações no tempo
nT = int(Tf / dt)
for t in range(nT):
    U = resolver_direcao_alternada(U, A_x, axis=0)  # Passo 1: resolver ao longo de x
    U = resolver_direcao_alternada(U, A_y, axis=1)  # Passo 2: resolver ao longo de y

# Mostrar e salvar o resultado final
plt.imshow(U, cmap='hot', extent=[0, Lx, 0, Ly])
plt.colorbar(label='Temperatura')
plt.title("Distribuição de Temperatura Final")
plt.show()

output_path = os.path.join('examples', 'heat_simulation_output.png')
plt.imsave(output_path, U, cmap='hot')
print(f"Imagem salva em: {output_path}")
