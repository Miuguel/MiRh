import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import colorsys
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para gerar imagens

# Importa as classes e funções do arquivo principal
from comp_graf_curved_surfaces import (
    Object3D, create_torus_with_specular_top, create_cube, create_sphere, 
    apply_transformations, create_butterfly,
    painter_algorithm
)

def render_scene_static(objects, elevation, azimuth, filename):
    """Renderiza a cena em um ângulo específico e salva como imagem"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Calcula direção de visualização baseada nos ângulos
    azim_rad = np.radians(azimuth)
    elev_rad = np.radians(elevation)
    
    # Direção de visualização (vetor unitário)
    view_direction = np.array([
        np.cos(elev_rad) * np.sin(azim_rad),
        np.cos(elev_rad) * np.cos(azim_rad),
        np.sin(elev_rad)
    ])
    
    # Aplica o algoritmo do pintor
    sorted_faces = painter_algorithm(objects, view_direction)
    
    # Renderiza as faces na ordem correta (mais distante primeiro)
    for face_info in sorted_faces:
        obj = objects[face_info['object_idx']]
        face = face_info['face']
        
        # Obtém vértices da face com posição do objeto
        face_vertices = [obj.vertices[idx] + obj.position for idx in face]
        
        # Calcula cor iluminada para esta face
        colors = obj.get_illuminated_colors(view_direction)
        face_color = colors[face_info['face_idx']]
        
        # Cria o polígono 3D
        polygon = Poly3DCollection([face_vertices], 
                                 facecolor=face_color, 
                                 edgecolor='black', 
                                 alpha=1.0,
                                 linewidth=0.5)
        ax.add_collection3d(polygon)
    
    # Configuração do gráfico 3D
    ax.set_xlim(-4, 1)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-2, 4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Cena 3D com Superfícies Curvas e Sombreamento de Phong\nElevação: {elevation}°, Azimute: {azimuth}°")
    
    # Define o ângulo de visualização
    ax.view_init(elev=elevation, azim=azimuth)
    
    # Salva a imagem
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Imagem salva: {filename}")

def main():
    """Função principal para gerar imagens da cena"""
    print("=== GERANDO IMAGENS DA CENA 3D ===")
    
    # Criação dos objetos
    torus = create_torus_with_specular_top(position=(-2, 0, 0), hue=240)
    borboleta_objects = create_butterfly()
    
    # Ajusta a posição da borboleta para ficar em cima do toro
    for obj in borboleta_objects:
        obj.position = np.array([-2, 0, 2])
    
    objects = [torus] + borboleta_objects
    
    # Ângulos de visualização para gerar imagens
    views = [
        (30, 45, "vista_frontal"),
        (30, 135, "vista_lateral_direita"),
        (30, 225, "vista_traseira"),
        (30, 315, "vista_lateral_esquerda"),
        (60, 45, "vista_superior"),
        (0, 45, "vista_inferior"),
        (45, 90, "vista_diagonal")
    ]
    
    # Gera imagens para cada ângulo
    for elevation, azimuth, name in views:
        filename = f"curved_surfaces_{name}.png"
        render_scene_static(objects, elevation, azimuth, filename)
    
    print("\n=== IMAGENS GERADAS COM SUCESSO ===")
    print("As imagens foram salvas no diretório atual com os seguintes nomes:")
    for _, _, name in views:
        print(f"  - curved_surfaces_{name}.png")

if __name__ == "__main__":
    main() 