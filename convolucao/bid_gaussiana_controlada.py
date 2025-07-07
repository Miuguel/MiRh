import numpy as np
from PIL import Image
from pathlib import Path
from scipy.linalg import svd, solve_sylvester
import matplotlib.pyplot as plt
from deconvolucao.utils import normalize_image, mse, psnr

# Caminhos
base_dir = Path(__file__).parent.parent
img_path = base_dir / 'exemplos' / 'cameraman_gauss_blur.png'

# 1. Carregar imagem borrada
def load_img(path):
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.float64) / 255.0

img_np = load_img(img_path)

# 2. Selecionar linhas/colunas centrais
h, w = img_np.shape
linha1 = img_np[h//2 - 2, :]
linha2 = img_np[h//2 + 2, :]
col1 = img_np[:, w//2 - 2]
col2 = img_np[:, w//2 + 2]

def sylvester_matrix(f, g):
    m = len(f) - 1
    n = len(g) - 1
    size = m + n
    F = np.pad(f, (0, size - m), 'constant')
    G = np.pad(g, (0, size - n), 'constant')
    S = np.zeros((size, size))
    for i in range(n):
        end = i + m + 1
        if end <= size and (end - i) == len(F):
            S[i, i:end] = F
    for i in range(m):
        end = i + n + 1
        if end <= size and (end - i) == len(G):
            S[n+i, i:end] = G
    return S

# 3. Definir grau do kernel próximo ao real (ex: 9)
grau_kernel = 9

# 4. Estimar PSF 1D para linhas
f = linha1[:grau_kernel]
g = linha2[:grau_kernel]
S = sylvester_matrix(f, g)
U, s, Vh = svd(S)
psf_1d = Vh[-1, :grau_kernel]
if np.sum(psf_1d) == 0:
    print('PSF 1D (linha) nula! Tente outras linhas ou outro grau.')
    psf_1d = np.ones(grau_kernel) / grau_kernel
else:
    psf_1d = psf_1d / np.sum(psf_1d)

# 5. Estimar PSF 1D para colunas
f_col = col1[:grau_kernel]
g_col = col2[:grau_kernel]
S_col = sylvester_matrix(f_col, g_col)
U_col, s_col, Vh_col = svd(S_col)
psf_1d_col = Vh_col[-1, :grau_kernel]
if np.sum(psf_1d_col) == 0:
    print('PSF 1D (coluna) nula! Tente outras colunas ou outro grau.')
    psf_1d_col = np.ones(grau_kernel) / grau_kernel
else:
    psf_1d_col = psf_1d_col / np.sum(psf_1d_col)

# 6. PSF 2D separável
psf_2d = np.outer(psf_1d_col, psf_1d)
psf_2d /= np.sum(psf_2d)

# 7. Deconvolução via Sylvester
psf_h, psf_w = psf_2d.shape
H_x = np.zeros((w, w))
H_y = np.zeros((h, h))
for i in range(w):
    H_x[i, max(0, i-psf_w+1):i+1] = psf_2d[0, :min(psf_w, i+1)][::-1]
for i in range(h):
    H_y[i, max(0, i-psf_h+1):i+1] = psf_2d[:min(psf_h, i+1), 0][::-1]
H_x += 1e-6 * np.eye(w)
H_y += 1e-6 * np.eye(h)
restaurada = solve_sylvester(H_y, H_x, img_np)
restaurada = normalize_image(restaurada)

# 8. Salvar e visualizar resultados
restaurada_uint8 = (np.clip(restaurada, 0, 1) * 255).astype(np.uint8)
Image.fromarray(restaurada_uint8).save(base_dir / 'exemplos' / 'cameraman_gauss_restaurada.png')
print('Imagem restaurada salva em exemplos/cameraman_gauss_restaurada.png')

plt.figure(figsize=(15,4))
plt.subplot(1,4,1)
plt.imshow(img_np, cmap='gray')
plt.title('Borrada')
plt.axis('off')
plt.subplot(1,4,2)
plt.imshow(restaurada, cmap='gray')
plt.title('Restaurada (BID)')
plt.axis('off')
plt.subplot(1,4,3)
plt.imshow(psf_2d, cmap='hot')
plt.title('PSF 2D estimada')
plt.axis('off')
plt.subplot(1,4,4)
plt.plot(psf_1d, label='Linha')
plt.plot(psf_1d_col, label='Coluna')
plt.title('Perfis PSF')
plt.legend()
plt.tight_layout()
plt.show() 