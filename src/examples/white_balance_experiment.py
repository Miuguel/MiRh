import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import colorspacious

class WhiteBalanceExperiment:
    """Experimento de balanço do branco"""
    
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Converte BGR para RGB
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # Iluminantes padrão (valores RGB)
        self.illuminants = {
            'D50': [0.9642, 1.0000, 0.8249],  # RGB aproximado
            'D55': [0.9568, 1.0000, 0.9214],
            'D65': [0.9504, 1.0000, 1.0888],
            'D75': [0.9497, 1.0000, 1.2264]
        }
        
        # Iluminantes no espaço XYZ
        self.illuminants_xyz = {
            'D50': [0.9642, 1.0000, 0.8249],
            'D55': [0.9568, 1.0000, 0.9214],
            'D65': [0.9504, 1.0000, 1.0888],
            'D75': [0.9497, 1.0000, 1.2264]
        }
    
    def select_white_region(self, x1, y1, x2, y2):
        """Seleciona região branca da imagem"""
        self.white_region = self.image_rgb[y1:y2, x1:x2]
        self.white_coords = (x1, y1, x2, y2)
        return self.white_region
    
    def calculate_average_white_rgb(self):
        """Calcula o valor RGB médio da região branca"""
        if not hasattr(self, 'white_region'):
            raise ValueError("Região branca não foi selecionada")
        
        # Calcula média RGB da região
        self.white_avg_rgb = np.mean(self.white_region, axis=(0, 1))
        print(f"Branco médio RGB: {self.white_avg_rgb}")
        return self.white_avg_rgb
    
    def apply_white_balance_rgb(self, target_illuminant):
        """Aplica balanço do branco no espaço RGB"""
        if not hasattr(self, 'white_avg_rgb'):
            self.calculate_average_white_rgb()
        
        # Calcula fatores de correção
        correction_factors = np.array(self.illuminants[target_illuminant]) / self.white_avg_rgb
        
        # Aplica correção
        corrected_image = self.image_rgb * correction_factors
        corrected_image = np.clip(corrected_image, 0, 255).astype(np.uint8)
        
        return corrected_image
    
    def apply_white_balance_xyz(self, target_illuminant):
        """Aplica balanço do branco no espaço XYZ"""
        if not hasattr(self, 'white_avg_rgb'):
            self.calculate_average_white_rgb()
        
        # Converte RGB para XYZ
        xyz_image = colorspacious.cspace_convert(self.image_rgb, "sRGB1", "XYZ1")
        
        # Calcula branco médio em XYZ
        white_avg_xyz = np.mean(xyz_image[self.white_coords[1]:self.white_coords[3], 
                                        self.white_coords[0]:self.white_coords[2]], axis=(0, 1))
        
        # Calcula fatores de correção em XYZ
        target_xyz = np.array(self.illuminants_xyz[target_illuminant])
        correction_factors_xyz = target_xyz / white_avg_xyz
        
        # Aplica correção em XYZ
        corrected_xyz = xyz_image * correction_factors_xyz
        
        # Converte de volta para RGB
        corrected_rgb = colorspacious.cspace_convert(corrected_xyz, "XYZ1", "sRGB1")
        corrected_rgb = np.clip(corrected_rgb * 255, 0, 255).astype(np.uint8)
        
        return corrected_rgb
    
    def visualize_results(self):
        """Visualiza os resultados do experimento"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Imagem original com região selecionada
        axes[0, 0].imshow(self.image_rgb)
        rect = Rectangle((self.white_coords[0], self.white_coords[1]), 
                        self.white_coords[2] - self.white_coords[0],
                        self.white_coords[3] - self.white_coords[1],
                        linewidth=2, edgecolor='red', facecolor='none')
        axes[0, 0].add_patch(rect)
        axes[0, 0].set_title('Imagem Original\n(Região branca selecionada)')
        axes[0, 0].axis('off')
        
        # Região branca ampliada
        axes[0, 1].imshow(self.white_region)
        axes[0, 1].set_title(f'Região Branca\nRGB médio: {self.white_avg_rgb.astype(int)}')
        axes[0, 1].axis('off')
        
        # Histograma RGB da região branca
        for i, color in enumerate(['R', 'G', 'B']):
            axes[0, 2].hist(self.white_region[:, :, i].flatten(), 
                           bins=50, alpha=0.7, label=color, color=['red', 'green', 'blue'][i])
        axes[0, 2].set_title('Histograma RGB da Região Branca')
        axes[0, 2].legend()
        axes[0, 2].set_xlabel('Valor RGB')
        axes[0, 2].set_ylabel('Frequência')
        
        # Resultados com diferentes iluminantes (RGB)
        for i, illuminant in enumerate(['D50', 'D65']):
            corrected = self.apply_white_balance_rgb(illuminant)
            axes[1, i].imshow(corrected)
            axes[1, i].set_title(f'Balanço RGB - {illuminant}')
            axes[1, i].axis('off')
        
        # Resultado com XYZ
        corrected_xyz = self.apply_white_balance_xyz('D65')
        axes[1, 2].imshow(corrected_xyz)
        axes[1, 2].set_title('Balanço XYZ - D65')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def save_results(self, output_dir="white_balance_results"):
        """Salva todos os resultados"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Salva imagem original
        plt.imsave(f"{output_dir}/original.png", self.image_rgb)
        
        # Salva resultados RGB
        for illuminant in self.illuminants.keys():
            corrected_rgb = self.apply_white_balance_rgb(illuminant)
            plt.imsave(f"{output_dir}/rgb_{illuminant}.png", corrected_rgb)
        
        # Salva resultados XYZ
        for illuminant in self.illuminants_xyz.keys():
            corrected_xyz = self.apply_white_balance_xyz(illuminant)
            plt.imsave(f"{output_dir}/xyz_{illuminant}.png", corrected_xyz)
        
        print(f"Resultados salvos em: {output_dir}/")

def main():
    """Função principal para demonstrar o experimento"""
    print("=== EXPERIMENTO DE BALANÇO DO BRANCO ===")
    print("Este programa demonstra o processo de balanço do branco.")
    print("Para usar com sua própria imagem:")
    print("1. Substitua 'sample_image.jpg' pelo caminho da sua imagem")
    print("2. Ajuste as coordenadas da região branca")
    print("3. Execute o programa")
    
    # Exemplo com imagem de teste (você deve substituir pela sua)
    try:
        # Cria uma imagem de teste se não existir
        test_image = np.ones((400, 600, 3), dtype=np.uint8) * 200
        test_image[100:300, 200:400] = [220, 210, 200]  # Região "branca" ligeiramente colorida
        cv2.imwrite("sample_image.jpg", cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR))
        
        # Inicializa o experimento
        experiment = WhiteBalanceExperiment("sample_image.jpg")
        
        # Seleciona região branca (ajuste para sua imagem)
        experiment.select_white_region(200, 100, 400, 300)
        
        # Calcula branco médio
        white_avg = experiment.calculate_average_white_rgb()
        
        # Visualiza resultados
        experiment.visualize_results()
        
        # Salva resultados
        experiment.save_results()
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Certifique-se de ter uma imagem válida ou ajuste o código para sua imagem.")

if __name__ == "__main__":
    main() 