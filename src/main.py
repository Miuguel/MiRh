from utils import extrair_canais_rgb
from conv_simulation import conv_simulation
from adi_simulation import adi_heat_simulation
from conv_FFT_simulation import conv_simulation_fft
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# Caminho dos arquivos
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_imagem = os.path.join(diretorio_atual, '../examples/example_image.png')
caminho_saida = os.path.join(diretorio_atual, '../examples/heat_simulation_output_FFT_blue.png')

# Extrair canais R, G, B
R, G, B = extrair_canais_rgb(caminho_imagem)
R, G, B = R.astype(float) / 255, G.astype(float) / 255, B.astype(float) / 255

# Parâmetros da simulação (0.25,40) - (10,1)
dt = 0.2
num_iterations_r, num_iterations_g, num_iterations_b = 0, 0, 100

# Simulação usando 
start_time = time.time()
matriz_r = conv_simulation(R, num_iterations_r, dt)
matriz_g = conv_simulation(G, num_iterations_g, dt)
matriz_b = conv_simulation(B, num_iterations_b, dt)
elapsed_time_fft = time.time() - start_time
print(f'Elapsed time: {elapsed_time_fft:.4f} seconds')

# Recriar e salvar imagem resultante
imagem_resultante = np.stack((matriz_r, matriz_g, matriz_b), axis=-1)
plt.imsave(caminho_saida, imagem_resultante)

# Exibir imagem resultante
plt.imshow(imagem_resultante)
plt.title('Simulação de Calor ')
plt.show()
