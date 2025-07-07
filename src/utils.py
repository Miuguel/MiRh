from PIL import Image
import numpy as np

def extrair_canais_rgb(caminho_imagem):
    """
    Carrega uma imagem e retorna os canais R, G, B em formato NumPy.
    """
    imagem = Image.open(caminho_imagem).convert('RGB')
    imagem_array = np.array(imagem)
    matriz_r = imagem_array[:, :, 0]  # Canal Red
    matriz_g = imagem_array[:, :, 1]  # Canal Green
    matriz_b = imagem_array[:, :, 2]  # Canal Blue
    return matriz_r, matriz_g, matriz_b
