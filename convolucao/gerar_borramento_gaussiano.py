import numpy as np
from PIL import Image
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Criar PSF gaussiana 2D normalizada
def gaussian_psf(size=9, sigma=2):
    ax = np.arange(-size // 2 + 1., size // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    psf = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    psf /= np.sum(psf)
    return psf

psf = gaussian_psf(size=9, sigma=2)

# 2. Carregar imagem
def get_img_path():
    base_dir = Path(__file__).parent.parent
    img_path = base_dir / 'exemplos' / 'cameraman.jpg'
    if not img_path.exists():
        raise FileNotFoundError(f'Imagem não encontrada: {img_path}')
    return img_path

img = Image.open(get_img_path()).convert('L')
img_np = np.array(img, dtype=np.float64) / 255.0

# 3. Convoluir imagem e PSF
img_blur = convolve2d(img_np, psf, mode='same', boundary='symm')

# 4. Visualizar e salvar resultado
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.imshow(img_np, cmap='gray')
plt.title('Original')
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(psf, cmap='hot')
plt.title('PSF Gaussiana')
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(img_blur, cmap='gray')
plt.title('Borrada')
plt.axis('off')
plt.tight_layout()
plt.show()

# Salvar imagem borrada
base_dir = Path(__file__).parent.parent
img_blur_uint8 = (np.clip(img_blur, 0, 1) * 255).astype(np.uint8)
Image.fromarray(img_blur_uint8).save(base_dir / 'exemplos' / 'cameraman_gauss_blur.png')
print('Imagem borrada salva em exemplos/cameraman_gauss_blur.png') 