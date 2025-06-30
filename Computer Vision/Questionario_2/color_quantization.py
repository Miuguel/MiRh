import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

def uniform_quantization(image, levels):
    """
    Aplica quantização uniforme com níveis especificados por canal
    """
    # Calcula o passo de quantização
    step = 256 // levels
    
    # Aplica quantização uniforme
    quantized = (image // step) * step
    
    return quantized

def kmeans_quantization(image, n_colors):
    """
    Aplica quantização não-uniforme usando K-means clustering
    """
    # Redimensiona a imagem para processamento mais rápido
    h, w, d = image.shape
    image_array = image.reshape(h * w, d)
    
    # Aplica K-means
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    labels = kmeans.fit_predict(image_array)
    
    # Substitui cada pixel pela cor do centroide mais próximo
    quantized_array = kmeans.cluster_centers_[labels]
    quantized_image = quantized_array.reshape(h, w, d)
    
    return quantized_image.astype(np.uint8)

def median_cut_quantization(image, n_colors):
    """
    Implementa quantização usando algoritmo Median Cut
    """
    def median_cut(pixels, depth):
        if depth == 0 or len(pixels) == 0:
            return [np.mean(pixels, axis=0)]
        
        # Encontra o canal com maior variância
        variances = np.var(pixels, axis=0)
        channel = np.argmax(variances)
        
        # Ordena pixels pelo canal com maior variância
        sorted_pixels = pixels[pixels[:, channel].argsort()]
        
        # Divide ao meio
        mid = len(sorted_pixels) // 2
        left = median_cut(sorted_pixels[:mid], depth - 1)
        right = median_cut(sorted_pixels[mid:], depth - 1)
        
        return left + right
    
    # Redimensiona para processamento
    h, w, d = image.shape
    pixels = image.reshape(h * w, d)
    
    # Calcula profundidade necessária
    depth = int(np.log2(n_colors))
    
    # Aplica median cut
    palette = median_cut(pixels, depth)
    palette = np.array(palette[:n_colors])
    
    # Encontra o centroide mais próximo para cada pixel
    quantized = np.zeros_like(pixels)
    for i, pixel in enumerate(pixels):
        distances = np.linalg.norm(palette - pixel, axis=1)
        closest = np.argmin(distances)
        quantized[i] = palette[closest]
    
    return quantized.reshape(h, w, d).astype(np.uint8)

def calculate_color_count(image):
    """
    Calcula o número de cores únicas na imagem
    """
    h, w, d = image.shape
    pixels = image.reshape(h * w, d)
    unique_colors = np.unique(pixels, axis=0)
    return len(unique_colors)

def main():
    # Carrega a imagem
    image_path = "IMG_20231123_230708.jpg"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    print(f"Imagem original carregada: {image.shape}")
    print(f"Número de cores únicas na imagem original: {calculate_color_count(image)}")
    
    # Salva imagem original
    cv2.imwrite("original_quantization.png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    # PARTE 1: Quantização Uniforme
    print("\n=== QUANTIZAÇÃO UNIFORME ===")
    
    levels_list = [128, 64, 32]
    for levels in levels_list:
        print(f"\nAplicando quantização uniforme com {levels} níveis por canal...")
        
        # Calcula quantas cores totais isso representa
        total_colors = levels ** 3
        print(f"Total de cores possíveis: {total_colors}")
        
        # Aplica quantização uniforme
        quantized = uniform_quantization(image, levels)
        
        # Calcula cores únicas resultantes
        unique_colors = calculate_color_count(quantized)
        print(f"Cores únicas resultantes: {unique_colors}")
        
        # Salva resultado
        filename = f"uniform_quantization_{levels}levels.png"
        cv2.imwrite(filename, cv2.cvtColor(quantized, cv2.COLOR_RGB2BGR))
        print(f"Salvo: {filename}")
    
    # PARTE 2: Quantização Não-Uniforme (Opcional)
    print("\n=== QUANTIZAÇÃO NÃO-UNIFORME ===")
    
    # Usa 32.768 cores (mesmo que a quantização uniforme de 32 níveis)
    target_colors = 32768
    
    print(f"\nAplicando quantização K-means com {target_colors} cores...")
    kmeans_quantized = kmeans_quantization(image, target_colors)
    unique_colors_kmeans = calculate_color_count(kmeans_quantized)
    print(f"Cores únicas resultantes (K-means): {unique_colors_kmeans}")
    cv2.imwrite("kmeans_quantization_32768.png", cv2.cvtColor(kmeans_quantized, cv2.COLOR_RGB2BGR))
    print("Salvo: kmeans_quantization_32768.png")
    
    print(f"\nAplicando quantização Median Cut com {target_colors} cores...")
    median_quantized = median_cut_quantization(image, target_colors)
    unique_colors_median = calculate_color_count(median_quantized)
    print(f"Cores únicas resultantes (Median Cut): {unique_colors_median}")
    cv2.imwrite("median_cut_quantization_32768.png", cv2.cvtColor(median_quantized, cv2.COLOR_RGB2BGR))
    print("Salvo: median_cut_quantization_32768.png")
    
    # Comparação visual
    print("\n=== COMPARAÇÃO VISUAL ===")
    print("Arquivos gerados:")
    print("- original_quantization.png")
    print("- uniform_quantization_128levels.png")
    print("- uniform_quantization_64levels.png") 
    print("- uniform_quantization_32levels.png")
    print("- kmeans_quantization_32768.png")
    print("- median_cut_quantization_32768.png")
    
    print("\nAnálise:")
    print("- A quantização uniforme pode causar perda de detalhes importantes")
    print("- A quantização não-uniforme (K-means e Median Cut) preserva melhor")
    print("  as cores mais frequentes na imagem")
    print("- K-means tende a ser mais lento mas produz resultados mais precisos")
    print("- Median Cut é mais rápido e ainda produz bons resultados")

if __name__ == "__main__":
    main() 