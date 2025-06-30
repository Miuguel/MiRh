import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def histogram_equalization(image):
    """
    Implementa equalização de histograma manualmente
    """
    # Converte para escala de cinza se necessário
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
    
    # Calcula histograma
    hist, bins = np.histogram(gray.flatten(), 256, [0, 256])
    
    # Calcula função de distribuição cumulativa
    cdf = hist.cumsum()
    cdf_normalized = cdf * 255 / cdf[-1]
    
    # Aplica equalização
    equalized = np.interp(gray.flatten(), bins[:-1], cdf_normalized)
    equalized = equalized.reshape(gray.shape).astype(np.uint8)
    
    return equalized

def median_filter(image, kernel_size):
    """
    Implementa filtro da mediana manualmente
    """
    # Garante que kernel_size é ímpar
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Calcula padding
    pad = kernel_size // 2
    
    # Adiciona padding à imagem
    padded = np.pad(image, pad, mode='reflect')
    
    # Inicializa imagem de saída
    filtered = np.zeros_like(image)
    
    # Aplica filtro da mediana
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Extrai região do kernel
            region = padded[i:i+kernel_size, j:j+kernel_size]
            # Calcula mediana
            filtered[i, j] = np.median(region)
    
    return filtered.astype(np.uint8)

def remove_spectral_noise(image):
    """
    Remove ruído espectral usando Transformada Discreta de Fourier
    """
    # Converte para escala de cinza se necessário
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()
    
    # Aplica FFT 2D
    f_transform = fft2(gray)
    f_shift = fftshift(f_transform)
    
    # Calcula magnitude do espectro
    magnitude_spectrum = np.log(np.abs(f_shift) + 1)
    
    # Cria máscara para remover ruído espectral
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    
    # Cria máscara passa-baixa (filtro gaussiano)
    mask = np.zeros((rows, cols), np.uint8)
    r = 30  # Raio do filtro (ajuste conforme necessário)
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 1
    
    # Aplica máscara no domínio da frequência
    f_shift_filtered = f_shift * mask
    
    # Aplica IFFT
    f_ishift = ifftshift(f_shift_filtered)
    img_back = ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # Normaliza para [0, 255]
    img_back = np.clip(img_back, 0, 255).astype(np.uint8)
    
    return img_back, magnitude_spectrum, mask

def plot_results(original, processed, title, filename):
    """
    Plota e salva resultados
    """
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(processed, cmap='gray')
    plt.title(title)
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("=== QUESTIONÁRIO 3 - PROCESSAMENTO DE IMAGENS ===\n")
    
    # PARTE 1: Equalização de Histograma
    print("1. Equalização de Histograma")
    print("Processando Questionario-3-Imagem-1.tif...")
    
    img1 = cv2.imread("Questionario-3-Imagem-1.tif", cv2.IMREAD_GRAYSCALE)
    if img1 is None:
        print("Erro: Não foi possível carregar Questionario-3-Imagem-1.tif")
        return
    
    equalized1 = histogram_equalization(img1)
    cv2.imwrite("equalized_image1.png", equalized1)
    plot_results(img1, equalized1, "Equalizada", "equalization_comparison1.png")
    print("Salvo: equalized_image1.png, equalization_comparison1.png")
    
    print("Processando Questionario-3-Imagem-2.tif...")
    img2 = cv2.imread("Questionario-3-Imagem-2.tif", cv2.IMREAD_GRAYSCALE)
    if img2 is None:
        print("Erro: Não foi possível carregar Questionario-3-Imagem-2.tif")
        return
    
    equalized2 = histogram_equalization(img2)
    cv2.imwrite("equalized_image2.png", equalized2)
    plot_results(img2, equalized2, "Equalizada", "equalization_comparison2.png")
    print("Salvo: equalized_image2.png, equalization_comparison2.png")
    
    # PARTE 2: Filtro da Mediana
    print("\n2. Filtro da Mediana")
    print("Processando Questionario-3-Imagem-3.tif...")
    
    img3 = cv2.imread("Questionario-3-Imagem-3.tif", cv2.IMREAD_GRAYSCALE)
    if img3 is None:
        print("Erro: Não foi possível carregar Questionario-3-Imagem-3.tif")
        return
    
    # Aplica filtros com diferentes tamanhos de kernel
    kernel_sizes = [3, 5, 7]
    for kernel_size in kernel_sizes:
        print(f"Aplicando filtro da mediana com kernel {kernel_size}x{kernel_size}...")
        filtered = median_filter(img3, kernel_size)
        cv2.imwrite(f"median_filter_{kernel_size}x{kernel_size}.png", filtered)
        plot_results(img3, filtered, f"Mediana {kernel_size}x{kernel_size}", 
                    f"median_comparison_{kernel_size}x{kernel_size}.png")
        print(f"Salvo: median_filter_{kernel_size}x{kernel_size}.png, median_comparison_{kernel_size}x{kernel_size}.png")
    
    # PARTE 3: Remoção de Ruído Espectral
    print("\n3. Remoção de Ruído Espectral")
    print("Processando Questionario-3-Imagem-4.png...")
    
    img4 = cv2.imread("Questionario-3-Imagem-4.png", cv2.IMREAD_GRAYSCALE)
    if img4 is None:
        print("Erro: Não foi possível carregar Questionario-3-Imagem-4.png")
        return
    
    # Remove ruído espectral
    denoised, magnitude_spectrum, mask = remove_spectral_noise(img4)
    
    # Salva resultados
    cv2.imwrite("denoised_image4.png", denoised)
    cv2.imwrite("magnitude_spectrum.png", (magnitude_spectrum * 255 / magnitude_spectrum.max()).astype(np.uint8))
    cv2.imwrite("frequency_mask.png", mask * 255)
    
    # Plota comparação
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img4, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Espectro de Frequência')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(denoised, cmap='gray')
    plt.title('Ruído Removido')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig("spectral_noise_removal.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Salvo: denoised_image4.png, magnitude_spectrum.png, frequency_mask.png, spectral_noise_removal.png")
    
    print("\n=== PROCESSAMENTO CONCLUÍDO ===")
    print("\nArquivos gerados:")
    print("Equalização de Histograma:")
    print("- equalized_image1.png, equalized_image2.png")
    print("- equalization_comparison1.png, equalization_comparison2.png")
    print("\nFiltro da Mediana:")
    print("- median_filter_3x3.png, median_filter_5x5.png, median_filter_7x7.png")
    print("- median_comparison_3x3.png, median_comparison_5x5.png, median_comparison_7x7.png")
    print("\nRemoção de Ruído Espectral:")
    print("- denoised_image4.png, magnitude_spectrum.png, frequency_mask.png")
    print("- spectral_noise_removal.png")

if __name__ == "__main__":
    main() 