from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import os

def extrair_canais_rgb(caminho_imagem):
    """
    Função que carrega uma imagem e retorna matrizes separadas para os canais de cor Red, Green e Blue.

    :param caminho_imagem: O caminho para a imagem a ser carregada.
    :return: Três matrizes NumPy correspondentes aos canais R, G e B.
    """
    # Carregar a imagem
    imagem = Image.open(caminho_imagem)
    
    # Converter a imagem para RGB caso não esteja nesse modo
    imagem_rgb = imagem.convert('RGB')
    
    # Converter a imagem para um array NumPy
    imagem_array = np.array(imagem_rgb)
    
    # Extrair os canais R, G, B
    matriz_r = imagem_array[:, :, 0]  # Canal Red
    matriz_g = imagem_array[:, :, 1]  # Canal Green
    matriz_b = imagem_array[:, :, 2]  # Canal Blue

    return matriz_r, matriz_g, matriz_b
def funcao_calor_otim_matrix(matrix, num_iterations, variacao):
    # Função para atualizar a matriz
    rows, cols = matrix.shape  # Tamanho da matriz

    for _ in range(num_iterations):
        # Criar matrizes deslocadas com NaN em vez de zeros
        matrix_up = np.vstack([matrix[1:, :], np.full((1, cols), np.nan)])
        matrix_down = np.vstack([np.full((1, cols), np.nan), matrix[:-1, :]])
        matrix_left = np.hstack([matrix[:, 1:], np.full((rows, 1), np.nan)])
        matrix_right = np.hstack([np.full((rows, 1), np.nan), matrix[:, :-1]])

        # Soma das matrizes deslocadas, ignorando NaNs
        sum_neighbors = np.nansum(np.stack([matrix_up, matrix_down, matrix_left, matrix_right], axis=0), axis=0)

        # Número de vizinhos válidos (não NaNs)
        num_neighbors = np.sum(~np.isnan(np.stack([matrix_up, matrix_down, matrix_left, matrix_right], axis=0)), axis=0)

        # Evitar divisão por zero, mas agora com NaNs não é necessário porque o np.nansum irá ignorá-los
        # num_neighbors[num_neighbors == 0] = 1

        # Calcular a nova matriz com a fórmula fornecida, agora ignorando NaNs corretamente
        new_matrix = matrix + variacao * (sum_neighbors / num_neighbors - matrix)

        # Atualizar a matriz original com a nova matriz
        matrix = new_matrix

    return matrix  # Retornar a matriz atualizada

# Nome do arquivo de imagem
nome_arquivo = 'grid_0.png'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Combinar o diretório atual com o nome do arquivo
caminho_imagem = os.path.join(diretorio_atual, nome_arquivo)
# Abrir a imagem
imagem = Image.open(caminho_imagem).convert('RGB')
imagem_array = np.array(imagem)
R = imagem_array[:, :, 0].astype(float) / 255
G = imagem_array[:, :, 1].astype(float) / 255
B = imagem_array[:, :, 2].astype(float) / 255

#print("Matriz do canal Red (R):\n", R)
#print("Matriz do canal Green (G):\n", G)
#print("Matriz do canal Blue (B):\n", B)

"""
plt.imshow(R, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("Vermelho")
plt.show()
"""

# Iniciar o cronômetro
start_time = time.time()

num_iterations_r = 0
num_iterations_g = 5
num_iterations_b = 0

variacao = 0.9  # Valor pequeno para a variação, menor que 1
matriz_r = funcao_calor_otim_matrix(R, num_iterations_r, variacao)
matriz_g = funcao_calor_otim_matrix(G, num_iterations_g, variacao)
matriz_b = funcao_calor_otim_matrix(B, num_iterations_b, variacao)
elapsed_time = time.time() - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')

"""
plt.imshow(matriz_r, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("Matriz iteração vermelho")
plt.show()
"""

# Recriar a imagem combinando as camadas R, G, B
imagem_recuperada = np.stack((matriz_r, matriz_g, matriz_b), axis=-1)

# Mostrar a imagem recuperada para comparação
plt.subplot(1, 2, 2)
plt.imshow(imagem_recuperada)
plt.title('Imagem Recuperada')

# Caminho para salvar a imagem recuperada
caminho_salvar_imagem = os.path.join(diretorio_atual, 'imagem_verde.png')

# Salvar a imagem recuperada
plt.imsave(caminho_salvar_imagem, imagem_recuperada)

plt.show()

# TODO: Adicionar Condição de Estabilidade, delta x e delta t, fazer o algoritmo do metodo implicito
# 2) Aprender a teoria da discretização no Apêndice do livro de EDP
# : Um Curso de Graduação (Valeria Iorio); ali tem Método Explícito ou Implícito vs Híbrido
