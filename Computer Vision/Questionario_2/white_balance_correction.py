import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import colorsys

def rgb_to_xyz(rgb):
    """Converte RGB para XYZ"""
    # Normaliza RGB para [0,1]
    rgb = rgb.astype(np.float64) / 255.0
    
    # Matriz de conversão RGB para XYZ (sRGB)
    transform_matrix = np.array([
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9505]
    ])
    
    # Aplica a transformação
    xyz = np.dot(rgb, transform_matrix.T)
    return xyz

def xyz_to_rgb(xyz):
    """Converte XYZ para RGB"""
    # Matriz de conversão XYZ para RGB (sRGB)
    transform_matrix = np.array([
        [3.2406, -1.5372, -0.4986],
        [-0.9689, 1.8758, 0.0415],
        [0.0557, -0.2040, 1.0570]
    ])
    
    # Aplica a transformação
    rgb = np.dot(xyz, transform_matrix.T)
    
    # Clipping para [0,1]
    rgb = np.clip(rgb, 0, 1)
    
    # Converte para [0,255]
    rgb = (rgb * 255).astype(np.uint8)
    return rgb

def calculate_white_point(image, region_coords):
    """Calcula o ponto branco médio em uma região da imagem"""
    x1, y1, x2, y2 = region_coords
    region = image[y1:y2, x1:x2]
    
    # Calcula a média RGB da região
    white_point_rgb = np.mean(region, axis=(0, 1))
    
    # Converte para XYZ
    white_point_xyz = rgb_to_xyz(white_point_rgb.reshape(1, 1, 3))
    white_point_xyz = white_point_xyz[0, 0]
    
    return white_point_rgb, white_point_xyz

def apply_white_balance_rgb(image, white_point, target_white):
    """Aplica correção de white balance no espaço RGB"""
    # Normaliza os pontos brancos
    white_point_norm = white_point / np.max(white_point)
    target_white_norm = target_white / np.max(target_white)
    
    # Calcula os fatores de correção
    correction_factors = target_white_norm / white_point_norm
    
    # Aplica a correção
    corrected_image = image.astype(np.float64) * correction_factors
    corrected_image = np.clip(corrected_image, 0, 255).astype(np.uint8)
    
    return corrected_image

def apply_white_balance_xyz(image, white_point_xyz, target_white_xyz):
    """Aplica correção de white balance no espaço XYZ"""
    # Converte imagem para XYZ
    xyz_image = rgb_to_xyz(image)
    
    # Calcula os fatores de correção
    correction_factors = target_white_xyz / white_point_xyz
    
    # Aplica a correção
    corrected_xyz = xyz_image * correction_factors
    
    # Converte de volta para RGB
    corrected_image = xyz_to_rgb(corrected_xyz)
    
    return corrected_image

def main():
    # Carrega a imagem
    image_path = "IMG_20231123_230708.jpg"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define a região do papel branco (coordenadas [x1, y1, x2, y2])
    # Você pode ajustar essas coordenadas manualmente
    paper_region = [100, 100, 300, 400]  # Exemplo - ajuste conforme sua imagem
    
    # Calcula o ponto branco
    white_point_rgb, white_point_xyz = calculate_white_point(image, paper_region)
    print(f"Ponto branco RGB detectado: {white_point_rgb}")
    print(f"Ponto branco XYZ detectado: {white_point_xyz}")
    
    # Iluminantes padrão (valores RGB aproximados)
    illuminants = {
        'D50': np.array([245, 245, 255]),  # Branco quente
        'D55': np.array([248, 248, 255]),  # Branco neutro
        'D65': np.array([255, 255, 255]),  # Branco padrão
        'D75': np.array([255, 255, 248])   # Branco frio
    }
    
    # Iluminantes XYZ (valores aproximados)
    illuminants_xyz = {
        'D50': np.array([0.9642, 1.0000, 0.8249]),
        'D55': np.array([0.9568, 1.0000, 0.9214]),
        'D65': np.array([0.9504, 1.0000, 1.0888]),
        'D75': np.array([0.9497, 1.0000, 1.2264])
    }
    
    # Aplica correção RGB
    print("\nAplicando correção RGB...")
    for name, target in illuminants.items():
        corrected_rgb = apply_white_balance_rgb(image, white_point_rgb, target)
        cv2.imwrite(f"white_balance_rgb_{name}.png", cv2.cvtColor(corrected_rgb, cv2.COLOR_RGB2BGR))
        print(f"Salvo: white_balance_rgb_{name}.png")
    
    # Aplica correção XYZ
    print("\nAplicando correção XYZ...")
    for name, target in illuminants_xyz.items():
        corrected_xyz = apply_white_balance_xyz(image, white_point_xyz, target)
        cv2.imwrite(f"white_balance_xyz_{name}.png", cv2.cvtColor(corrected_xyz, cv2.COLOR_RGB2BGR))
        print(f"Salvo: white_balance_xyz_{name}.png")
    
    # Salva imagem original para comparação
    cv2.imwrite("original_image.png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    print("\nProcessamento concluído!")
    print("Arquivos gerados:")
    print("- original_image.png")
    print("- white_balance_rgb_D50.png, white_balance_rgb_D55.png, white_balance_rgb_D65.png, white_balance_rgb_D75.png")
    print("- white_balance_xyz_D50.png, white_balance_xyz_D55.png, white_balance_xyz_D65.png, white_balance_xyz_D75.png")

if __name__ == "__main__":
    main() 