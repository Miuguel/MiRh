import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

class ColorQuantizationExperiment:
    """Experimento de quantização de cores"""
    
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Converte BGR para RGB
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.height, self.width = self.image_rgb.shape[:2]
        
        # Níveis de quantização
        self.quantization_levels = [128, 64, 32]
        
    def uniform_quantization(self, levels):
        """Quantização uniforme com níveis igualmente espaçados"""
        # Calcula o passo de quantização
        step = 256 // levels
        
        # Aplica quantização
        quantized = (self.image_rgb // step) * step
        
        # Adiciona metade do passo para centralizar
        quantized = quantized + step // 2
        
        # Garante que os valores estejam no intervalo [0, 255]
        quantized = np.clip(quantized, 0, 255).astype(np.uint8)
        
        return quantized
    
    def kmeans_quantization(self, n_colors):
        """Quantização usando K-means para distribuição não uniforme"""
        # Reshape da imagem para lista de pixels
        pixels = self.image_rgb.reshape(-1, 3)
        
        # Aplica K-means
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        
        # Substitui cada pixel pelo centro do cluster
        quantized_pixels = kmeans.cluster_centers_[labels]
        
        # Reshape de volta para formato de imagem
        quantized = quantized_pixels.reshape(self.height, self.width, 3)
        quantized = np.clip(quantized, 0, 255).astype(np.uint8)
        
        return quantized, kmeans.cluster_centers_
    
    def calculate_color_statistics(self, image):
        """Calcula estatísticas de cores da imagem"""
        # Reshape para lista de pixels
        pixels = image.reshape(-1, 3)
        
        # Conta cores únicas
        unique_colors = np.unique(pixels, axis=0)
        n_unique_colors = len(unique_colors)
        
        # Calcula entropia de cores
        color_counts = Counter(map(tuple, pixels))
        total_pixels = len(pixels)
        entropy = 0
        for count in color_counts.values():
            p = count / total_pixels
            if p > 0:
                entropy -= p * np.log2(p)
        
        return {
            'unique_colors': n_unique_colors,
            'entropy': entropy,
            'total_pixels': total_pixels
        }
    
    def visualize_results(self):
        """Visualiza os resultados da quantização"""
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        
        # Imagem original
        axes[0, 0].imshow(self.image_rgb)
        axes[0, 0].set_title('Imagem Original')
        axes[0, 0].axis('off')
        
        # Histograma da imagem original
        for i, color in enumerate(['R', 'G', 'B']):
            axes[0, 1].hist(self.image_rgb[:, :, i].flatten(), 
                           bins=50, alpha=0.7, label=color, color=['red', 'green', 'blue'][i])
        axes[0, 1].set_title('Histograma Original')
        axes[0, 1].legend()
        axes[0, 1].set_xlabel('Valor RGB')
        axes[0, 1].set_ylabel('Frequência')
        
        # Quantização uniforme
        for i, levels in enumerate(self.quantization_levels):
            quantized = self.uniform_quantization(levels)
            axes[0, i+2].imshow(quantized)
            axes[0, i+2].set_title(f'Quantização Uniforme\n{levels} níveis')
            axes[0, i+2].axis('off')
        
        # K-means quantização
        for i, levels in enumerate(self.quantization_levels):
            quantized_kmeans, centers = self.kmeans_quantization(levels)
            axes[1, i+1].imshow(quantized_kmeans)
            axes[1, i+1].set_title(f'K-means Quantização\n{levels} cores')
            axes[1, i+1].axis('off')
        
        # Comparação de paletas de cores
        axes[1, 0].set_title('Comparação de Paletas')
        axes[1, 0].axis('off')
        
        # Mostra paletas de cores
        y_offset = 0.8
        for i, levels in enumerate(self.quantization_levels):
            # Paleta uniforme
            uniform = self.uniform_quantization(levels)
            unique_uniform = np.unique(uniform.reshape(-1, 3), axis=0)
            
            # Paleta K-means
            _, centers = self.kmeans_quantization(levels)
            
            # Desenha paletas
            for j, color in enumerate(unique_uniform[:10]):  # Mostra apenas 10 cores
                rect = plt.Rectangle((j*0.08, y_offset), 0.07, 0.15, 
                                   facecolor=color/255, edgecolor='black')
                axes[1, 0].add_patch(rect)
            
            axes[1, 0].text(0, y_offset-0.05, f'Uniforme {levels}:', fontsize=8)
            y_offset -= 0.25
            
            for j, color in enumerate(centers[:10]):
                rect = plt.Rectangle((j*0.08, y_offset), 0.07, 0.15, 
                                   facecolor=color/255, edgecolor='black')
                axes[1, 0].add_patch(rect)
            
            axes[1, 0].text(0, y_offset-0.05, f'K-means {levels}:', fontsize=8)
            y_offset -= 0.25
        
        axes[1, 0].set_xlim(0, 1)
        axes[1, 0].set_ylim(0, 1)
        
        plt.tight_layout()
        plt.show()
    
    def compare_methods(self):
        """Compara os métodos de quantização"""
        print("=== COMPARAÇÃO DE MÉTODOS DE QUANTIZAÇÃO ===")
        print(f"Imagem original: {self.width}x{self.height} pixels")
        
        # Estatísticas da imagem original
        orig_stats = self.calculate_color_statistics(self.image_rgb)
        print(f"\nImagem Original:")
        print(f"  - Cores únicas: {orig_stats['unique_colors']}")
        print(f"  - Entropia: {orig_stats['entropy']:.2f} bits")
        
        print("\nQuantização Uniforme:")
        for levels in self.quantization_levels:
            quantized = self.uniform_quantization(levels)
            stats = self.calculate_color_statistics(quantized)
            print(f"  {levels} níveis: {stats['unique_colors']} cores, entropia: {stats['entropy']:.2f}")
        
        print("\nQuantização K-means:")
        for levels in self.quantization_levels:
            quantized, centers = self.kmeans_quantization(levels)
            stats = self.calculate_color_statistics(quantized)
            print(f"  {levels} cores: {stats['unique_colors']} cores, entropia: {stats['entropy']:.2f}")
    
    def save_results(self, output_dir="quantization_results"):
        """Salva todos os resultados"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Salva imagem original
        plt.imsave(f"{output_dir}/original.png", self.image_rgb)
        
        # Salva quantização uniforme
        for levels in self.quantization_levels:
            quantized = self.uniform_quantization(levels)
            plt.imsave(f"{output_dir}/uniform_{levels}.png", quantized)
        
        # Salva quantização K-means
        for levels in self.quantization_levels:
            quantized, centers = self.kmeans_quantization(levels)
            plt.imsave(f"{output_dir}/kmeans_{levels}.png", quantized)
            
            # Salva paleta de cores
            palette = np.array(centers, dtype=np.uint8)
            palette_image = np.tile(palette, (50, 1, 1))
            plt.imsave(f"{output_dir}/palette_{levels}.png", palette_image)
        
        print(f"Resultados salvos em: {output_dir}/")

def create_test_image():
    """Cria uma imagem de teste com muitas cores"""
    height, width = 400, 600
    
    # Cria gradientes coloridos
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Gradiente vermelho-verde
    for i in range(height):
        for j in range(width):
            image[i, j, 0] = int(255 * i / height)  # Vermelho
            image[i, j, 1] = int(255 * j / width)   # Verde
            image[i, j, 2] = int(255 * (i + j) / (height + width))  # Azul
    
    # Adiciona algumas áreas sólidas
    image[50:100, 50:150] = [255, 0, 0]    # Vermelho
    image[150:200, 200:300] = [0, 255, 0]  # Verde
    image[250:300, 350:450] = [0, 0, 255]  # Azul
    image[350:380, 100:200] = [255, 255, 0]  # Amarelo
    
    return image

def main():
    """Função principal para demonstrar o experimento"""
    print("=== EXPERIMENTO DE QUANTIZAÇÃO DE CORES ===")
    print("Este programa demonstra diferentes métodos de quantização de cores.")
    print("Para usar com sua própria imagem:")
    print("1. Substitua 'sample_image.jpg' pelo caminho da sua imagem")
    print("2. Execute o programa")
    
    try:
        # Cria imagem de teste se não existir
        test_image = create_test_image()
        cv2.imwrite("sample_image.jpg", cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR))
        
        # Inicializa o experimento
        experiment = ColorQuantizationExperiment("sample_image.jpg")
        
        # Compara métodos
        experiment.compare_methods()
        
        # Visualiza resultados
        experiment.visualize_results()
        
        # Salva resultados
        experiment.save_results()
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Certifique-se de ter uma imagem válida ou ajuste o código para sua imagem.")

if __name__ == "__main__":
    main() 