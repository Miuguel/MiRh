import numpy as np

def normalize_image(img):
    """
    Normaliza uma imagem para o intervalo [0, 1].
    """
    img = np.asarray(img, dtype=np.float64)
    min_val = img.min()
    max_val = img.max()
    if max_val - min_val == 0:
        return np.zeros_like(img)
    return (img - min_val) / (max_val - min_val)

def mse(img1, img2):
    """
    Calcula o erro quadrático médio entre duas imagens.
    """
    return np.mean((np.asarray(img1) - np.asarray(img2)) ** 2)

def psnr(img1, img2):
    """
    Calcula o PSNR entre duas imagens.
    """
    mse_val = mse(img1, img2)
    if mse_val == 0:
        return float('inf')
    return 10 * np.log10(1.0 / mse_val)

def pad_coefficients(coeffs, length):
    """
    Preenche um vetor de coeficientes com zeros até o tamanho desejado.
    """
    coeffs = np.asarray(coeffs)
    if len(coeffs) >= length:
        return coeffs[:length]
    return np.pad(coeffs, (0, length - len(coeffs)), 'constant') 