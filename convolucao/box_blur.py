import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.signal import convolve

# Caminhos
base_dir = Path(__file__).parent.parent
img_path = base_dir / 'exemplos' / 'cameraman.jpg'

# 1. Carregar imagem original
def load_img(path):
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.float64) / 255.0

img_np = load_img(img_path)

# 2. Criar PSF box 1D
tamanho_kernel = 5
psf = np.ones(tamanho_kernel) / tamanho_kernel  # Box blur de tamanho 5

# 3. Aplicar box blur 1D em cada linha
def apply_box_blur_1d(img, psf):
    img_blur = np.zeros_like(img)
    for i in range(img.shape[0]):
        img_blur[i, :] = convolve(img[i, :], psf, mode='same')
    return img_blur

img_blur = apply_box_blur_1d(img_np, psf)

# 4. Salvar imagem borrada
img_blur_uint8 = (np.clip(img_blur, 0, 1) * 255).astype(np.uint8)
blur_path = base_dir / 'exemplos' / f'cameraman_box_blur_{tamanho_kernel}.png'
Image.fromarray(img_blur_uint8).save(blur_path)
print(f'Imagem borrada salva em {blur_path}') 