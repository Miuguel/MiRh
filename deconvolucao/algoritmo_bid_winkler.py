import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image
from scipy.linalg import svd, solve_sylvester
import matplotlib.pyplot as plt
from utils import normalize_image, mse, psnr

# Caminhos
base_dir = Path(__file__).parent.parent
img_path = base_dir / 'exemplos' / 'cameraman_box_blur_5.png'
img_orig_path = base_dir / 'exemplos' / 'cameraman.jpg'

# 1. Carregar imagem borrada e original
def load_img(path):
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.float64) / 255.0

img_blur = load_img(img_path)
img_orig = load_img(img_orig_path)

# 2. Usar apenas um par de linhas centrais
h = img_blur.shape[0]
grau_kernel = 5
linha1 = img_blur[h//2 - 1, :grau_kernel]
linha2 = img_blur[h//2 + 1, :grau_kernel]

# 3. Matriz de Sylvester
m = len(linha1) - 1
n = len(linha2) - 1
size = m + n
F = np.pad(linha1, (0, size - m), 'constant')
G = np.pad(linha2, (0, size - n), 'constant')
S = np.zeros((size, size))
for k in range(n):
    end = k + m + 1
    if end <= size and (end - k) == len(F):
        S[k, k:end] = F
for k in range(m):
    end = k + n + 1
    if end <= size and (end - k) == len(G):
        S[n+k, k:end] = G
U, s, Vh = svd(S)
psf_1d_est = Vh[-1, :grau_kernel]
if np.sum(psf_1d_est) != 0:
    psf_1d_est = psf_1d_est / np.sum(psf_1d_est)
else:
    psf_1d_est = np.ones(grau_kernel) / grau_kernel

# 4. PSF 2D separável (apenas linha, pois o blur é 1D)
psf_2d_est = np.outer(np.ones_like(psf_1d_est), psf_1d_est)
psf_2d_est /= np.sum(psf_2d_est)

# 5. Deconvolução via Sylvester
h, w = img_blur.shape
psf_h, psf_w = psf_2d_est.shape
H_x = np.zeros((w, w))
H_y = np.eye(h)  # Identidade, pois o blur é só em linhas
for i in range(w):
    H_x[i, max(0, i-psf_w+1):i+1] = psf_2d_est[0, :min(psf_w, i+1)][::-1]
H_x += 1e-6 * np.eye(w)
restaurada = solve_sylvester(H_y, H_x, img_blur)
restaurada = normalize_image(restaurada)

# 6. Salvar e visualizar resultados
restaurada_uint8 = (np.clip(restaurada, 0, 1) * 255).astype(np.uint8)
rest_path = base_dir / 'exemplos' / 'cameraman_box_restaurada.png'
Image.fromarray(restaurada_uint8).save(rest_path)
print(f'Imagem restaurada salva em {rest_path}')

plt.figure(figsize=(15,4))
plt.subplot(1,4,1)
plt.imshow(img_orig, cmap='gray')
plt.title('Original')
plt.axis('off')
plt.subplot(1,4,2)
plt.imshow(img_blur, cmap='gray')
plt.title('Box Blur')
plt.axis('off')
plt.subplot(1,4,3)
plt.imshow(restaurada, cmap='gray')
plt.title('Restaurada (BID)')
plt.axis('off')
plt.subplot(1,4,4)
plt.plot(np.ones(grau_kernel)/grau_kernel, label='PSF real')
plt.plot(psf_1d_est, label='PSF estimada')
plt.title('PSF real vs estimada')
plt.legend()
plt.tight_layout()
plt.show() 