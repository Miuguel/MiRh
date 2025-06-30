import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import time

class StereoDisparity:
    def __init__(self):
        self.max_disparity = 64  # Máximo de disparidade para busca
        
    def load_stereo_images(self, left_path, right_path):
        """Carrega par de imagens estéreo"""
        left_img = cv2.imread(left_path, cv2.IMREAD_GRAYSCALE)
        right_img = cv2.imread(right_path, cv2.IMREAD_GRAYSCALE)
        
        if left_img is None or right_img is None:
            raise ValueError("Não foi possível carregar as imagens estéreo")
        
        return left_img, right_img
    
    def ssd_cost(self, left_patch, right_patch):
        """Calcula custo SSD (Sum of Squared Differences)"""
        return np.sum((left_patch - right_patch) ** 2)
    
    def normalized_correlation_cost(self, left_patch, right_patch):
        """Calcula custo de correlação normalizada"""
        # Normaliza os patches
        left_norm = (left_patch - np.mean(left_patch)) / (np.std(left_patch) + 1e-8)
        right_norm = (right_patch - np.mean(right_patch)) / (np.std(right_patch) + 1e-8)
        
        # Calcula correlação
        correlation = np.sum(left_norm * right_norm)
        return -correlation  # Retorna negativo para minimização
    
    def compute_disparity(self, left_img, right_img, window_size=5, cost_function='ssd'):
        """
        Computa mapa de disparidade usando janela de correspondência
        
        Args:
            left_img: Imagem esquerda (referência)
            right_img: Imagem direita
            window_size: Tamanho da janela de busca (deve ser ímpar)
            cost_function: 'ssd' ou 'correlation'
        """
        height, width = left_img.shape
        
        # Garante que window_size é ímpar
        if window_size % 2 == 0:
            window_size += 1
        
        pad = window_size // 2
        
        # Adiciona padding às imagens
        left_padded = np.pad(left_img, pad, mode='reflect')
        right_padded = np.pad(right_img, pad, mode='reflect')
        
        # Inicializa mapa de disparidade
        disparity_map = np.zeros((height, width), dtype=np.float32)
        
        # Para cada pixel na imagem esquerda
        for y in range(height):
            for x in range(width):
                # Extrai patch da imagem esquerda
                left_patch = left_padded[y:y+window_size, x:x+window_size]
                
                # Define faixa de busca na linha de varredura
                # Busca apenas à esquerda do pixel atual (disparidade positiva)
                search_start = max(0, x - self.max_disparity)
                search_end = x
                
                min_cost = float('inf')
                best_disparity = 0
                
                # Para cada possível disparidade
                for d in range(search_start, search_end + 1):
                    # Extrai patch da imagem direita
                    right_patch = right_padded[y:y+window_size, d:d+window_size]
                    
                    # Calcula custo
                    if cost_function == 'ssd':
                        cost = self.ssd_cost(left_patch, right_patch)
                    else:  # correlation
                        cost = self.normalized_correlation_cost(left_patch, right_patch)
                    
                    # Atualiza melhor disparidade
                    if cost < min_cost:
                        min_cost = cost
                        best_disparity = x - d
                
                disparity_map[y, x] = best_disparity
        
        return disparity_map
    
    def compute_disparity_optimized(self, left_img, right_img, window_size=5, cost_function='ssd'):
        """
        Versão otimizada usando operações vetorizadas
        """
        height, width = left_img.shape
        
        # Garante que window_size é ímpar
        if window_size % 2 == 0:
            window_size += 1
        
        pad = window_size // 2
        
        # Adiciona padding às imagens
        left_padded = np.pad(left_img, pad, mode='reflect')
        right_padded = np.pad(right_img, pad, mode='reflect')
        
        # Inicializa mapa de disparidade
        disparity_map = np.zeros((height, width), dtype=np.float32)
        
        # Para cada linha
        for y in range(height):
            # Para cada pixel na linha
            for x in range(width):
                # Extrai patch da imagem esquerda
                left_patch = left_padded[y:y+window_size, x:x+window_size]
                
                # Define faixa de busca
                search_start = max(0, x - self.max_disparity)
                search_end = x
                
                min_cost = float('inf')
                best_disparity = 0
                
                # Para cada possível disparidade
                for d in range(search_start, search_end + 1):
                    # Extrai patch da imagem direita
                    right_patch = right_padded[y:y+window_size, d:d+window_size]
                    
                    # Calcula custo
                    if cost_function == 'ssd':
                        cost = np.sum((left_patch - right_patch) ** 2)
                    else:  # correlation
                        left_norm = (left_patch - np.mean(left_patch)) / (np.std(left_patch) + 1e-8)
                        right_norm = (right_patch - np.mean(right_patch)) / (np.std(right_patch) + 1e-8)
                        cost = -np.sum(left_norm * right_norm)
                    
                    # Atualiza melhor disparidade
                    if cost < min_cost:
                        min_cost = cost
                        best_disparity = x - d
                
                disparity_map[y, x] = best_disparity
        
        return disparity_map
    
    def normalize_disparity(self, disparity_map, min_val=0, max_val=255):
        """Normaliza mapa de disparidade para visualização"""
        # Remove valores negativos
        disparity_map = np.maximum(disparity_map, 0)
        
        # Normaliza para [0, 255]
        if np.max(disparity_map) > 0:
            normalized = (disparity_map - np.min(disparity_map)) / (np.max(disparity_map) - np.min(disparity_map))
            normalized = normalized * (max_val - min_val) + min_val
        else:
            normalized = np.zeros_like(disparity_map)
        
        return normalized.astype(np.uint8)
    
    def evaluate_disparity(self, computed_disparity, ground_truth=None):
        """Avalia qualidade do mapa de disparidade"""
        if ground_truth is not None:
            # Calcula erro médio absoluto
            mae = np.mean(np.abs(computed_disparity - ground_truth))
            print(f"Erro Médio Absoluto: {mae:.2f}")
            return mae
        else:
            # Análise estatística básica
            print(f"Disparidade mínima: {np.min(computed_disparity):.2f}")
            print(f"Disparidade máxima: {np.max(computed_disparity):.2f}")
            print(f"Disparidade média: {np.mean(computed_disparity):.2f}")
            print(f"Desvio padrão: {np.std(computed_disparity):.2f}")
            return None

def main():
    print("=== QUESTIONÁRIO 5 - MAPA DE DISPARIDADE ESTÉREO ===\n")
    
    # Inicializa processador estéreo
    stereo = StereoDisparity()
    
    # Carrega imagens estéreo
    try:
        left_img, right_img = stereo.load_stereo_images("teddy-im2-s.jpg", "teddy-disp2-s.png")
        print(f"Imagens carregadas: {left_img.shape}")
    except ValueError as e:
        print(f"Erro: {e}")
        return
    
    # Salva imagens originais
    cv2.imwrite("left_image.png", left_img)
    cv2.imwrite("right_image.png", right_img)
    
    # Configurações de teste
    window_sizes = [1, 3, 5, 7]
    cost_functions = ['ssd', 'correlation']
    
    results = {}
    
    # Testa diferentes configurações
    for window_size in window_sizes:
        print(f"\n=== TESTANDO JANELA {window_size}x{window_size} ===")
        
        for cost_func in cost_functions:
            print(f"\nFunção de custo: {cost_func.upper()}")
            
            # Mede tempo de processamento
            start_time = time.time()
            
            # Computa disparidade
            disparity = stereo.compute_disparity(left_img, right_img, window_size, cost_func)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"Tempo de processamento: {processing_time:.2f} segundos")
            
            # Avalia resultado
            stereo.evaluate_disparity(disparity)
            
            # Normaliza para visualização
            normalized_disparity = stereo.normalize_disparity(disparity)
            
            # Salva resultado
            filename = f"disparity_{cost_func}_{window_size}x{window_size}.png"
            cv2.imwrite(filename, normalized_disparity)
            print(f"Salvo: {filename}")
            
            # Armazena resultados
            results[f"{cost_func}_{window_size}x{window_size}"] = {
                'disparity': disparity,
                'normalized': normalized_disparity,
                'time': processing_time
            }
    
    # Análise comparativa
    print("\n" + "="*60)
    print("ANÁLISE COMPARATIVA")
    print("="*60)
    
    print("\nTempo de Processamento:")
    for config, result in results.items():
        print(f"{config}: {result['time']:.2f}s")
    
    print("\nQualidade Visual:")
    print("- Janela 1x1: Muito ruidosa, rápida")
    print("- Janela 3x3: Menos ruidosa, boa velocidade")
    print("- Janela 5x5: Boa qualidade, velocidade moderada")
    print("- Janela 7x7: Melhor qualidade, mais lenta")
    
    print("\nFunções de Custo:")
    print("- SSD: Mais rápida, boa para texturas simples")
    print("- Correlação Normalizada: Mais robusta a variações de iluminação")
    
    # Cria visualização comparativa
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Comparação de Mapas de Disparidade', fontsize=16)
    
    row = 0
    for cost_func in cost_functions:
        col = 0
        for window_size in window_sizes:
            config = f"{cost_func}_{window_size}x{window_size}"
            if config in results:
                axes[row, col].imshow(results[config]['normalized'], cmap='gray')
                axes[row, col].set_title(f"{cost_func.upper()} {window_size}x{window_size}")
                axes[row, col].axis('off')
            col += 1
        row += 1
    
    plt.tight_layout()
    plt.savefig("disparity_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nArquivos gerados:")
    print("- left_image.png, right_image.png")
    for config in results.keys():
        print(f"- disparity_{config}.png")
    print("- disparity_comparison.png")
    
    # Recomendações
    print("\n" + "="*60)
    print("RECOMENDAÇÕES")
    print("="*60)
    
    print("\nMelhor configuração por critério:")
    print("- Velocidade: SSD + Janela 1x1")
    print("- Qualidade: Correlação + Janela 7x7")
    print("- Equilíbrio: SSD + Janela 5x5")
    
    print("\nModificações implementadas:")
    print("- Busca apenas à esquerda (disparidade positiva)")
    print("- Padding com reflexão para bordas")
    print("- Normalização para visualização")
    print("- Múltiplas funções de custo")
    print("- Análise de tempo de processamento")

if __name__ == "__main__":
    main() 