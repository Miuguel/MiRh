from utils import extrair_canais_rgb
from heat_simulation import funcao_calor_otim_matrix
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# Caminho dos arquivos
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_imagem = os.path.join(diretorio_atual, '../examples/example_image.png')
caminho_saida = os.path.join(diretorio_atual, '../examples/heat_simulation_output.png')

# Extrair canais R, G, B
R, G, B = extrair_canais_rgb(caminho_imagem)
R, G, B = R.astype(float) / 255, G.astype(float) / 255, B.astype(float) / 255

# Parâmetros da simulação
variacao = 0.8366289
num_iterations_r, num_iterations_g, num_iterations_b = 0, 50, 0

# Iniciar simulação
start_time = time.time()
matriz_r = funcao_calor_otim_matrix(R, num_iterations_r, variacao)
matriz_g = funcao_calor_otim_matrix(G, num_iterations_g, variacao)
matriz_b = funcao_calor_otim_matrix(B, num_iterations_b, variacao)
elapsed_time = time.time() - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')

# Recriar e salvar imagem resultante
imagem_resultante = np.stack((matriz_r, matriz_g, matriz_b), axis=-1)
plt.imsave(caminho_saida, imagem_resultante)

# Exibir imagem resultante
plt.imshow(imagem_resultante)
plt.title('Simulação de Calor - Canal Verde')
plt.show()
