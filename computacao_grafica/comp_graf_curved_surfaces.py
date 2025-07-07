import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import colorsys
import matplotlib
matplotlib.use('TkAgg')  # Usar backend TkAgg para melhor suporte

class Object3D:
    """Classe para representar um objeto 3D com iluminação realista"""
    
    def __init__(self, vertices, faces, position=(0, 0, 0), hue=240, material_type="diffuse"):
        self.vertices = np.array(vertices)
        self.faces = faces
        self.position = np.array(position)
        self.hue = hue  # Hue fixo para todas as faces
        self.material_type = material_type  # "diffuse" ou "specular"
        
        # Calcula normais das faces
        self.face_normals = self._calculate_face_normals()
        
        # Parâmetros de iluminação para superfícies difusas
        self.ambient_light = 0.3  # Luz ambiente (seção 5.4.1)
        self.diffuse_light = 0.7  # Luz difusa
        
        # Parâmetros de iluminação para superfícies especulares (Phong)
        self.specular_light = 0.8  # Intensidade da luz especular
        self.shininess = 32  # Expoente de brilho (n na seção 5.4.4.3)
        
        # Luz amarelada conforme tabela 5.1 (RGB aproximado para luz amarelada)
        self.light_color = np.array([1.0, 0.9, 0.7])  # Luz amarelada
        self.light_direction = np.array([0, 0, 1])  # Luz vindo de frente (z positivo)
        
    def _calculate_face_normals(self):
        """Calcula as normais de cada face"""
        normals = []
        for face in self.faces:
            # Pega 3 vértices da face para calcular a normal
            v1 = self.vertices[face[0]]
            v2 = self.vertices[face[1]]
            v3 = self.vertices[face[2]]
            
            # Calcula vetores da face
            vec1 = v2 - v1
            vec2 = v3 - v1
            
            # Produto vetorial para obter a normal
            normal = np.cross(vec1, vec2)
            normal = normal / np.linalg.norm(normal)  # Normaliza
            
            normals.append(normal)
        return np.array(normals)
    
    def get_illuminated_colors(self, view_direction):
        """Calcula as cores iluminadas para cada face baseado no modelo de Phong"""
        colors = []
        
        for i, face in enumerate(self.faces):
            # Normal da face
            normal = self.face_normals[i]
            
            # Determina o material da face (especular ou difuso)
            face_material = getattr(self, 'face_materials', {}).get(i, self.material_type)
            
            # Calcula o ângulo entre a normal da face e a direção da luz
            cos_angle = np.dot(normal, self.light_direction)
            cos_angle = max(0, cos_angle)  # Não permite valores negativos
            
            if face_material == "diffuse":
                # Modelo de iluminação difusa (seção 5.4.3)
                # I = Ia + Id * cos(θ), onde Ia é luz ambiente e Id é luz difusa
                intensity = self.ambient_light + self.diffuse_light * cos_angle
                
                # Ajusta saturação baseada na intensidade (mais intenso = menos saturado)
                saturation = 1.0 - (intensity * 0.3)  # Mantém alguma saturação
                
                # Converte HSV para RGB
                rgb = colorsys.hsv_to_rgb(self.hue / 360.0, saturation, intensity)
                colors.append(rgb)
                
            elif face_material == "specular":
                # Modelo de iluminação de Phong com reflexão especular (seção 5.4.4.3)
                # I = Ia + Id * cos(θ) + Is * (cos(α))^n
                
                # Componente ambiente
                ambient_intensity = self.ambient_light
                
                # Componente difusa
                diffuse_intensity = self.diffuse_light * cos_angle
                
                # Componente especular (reflexão especular)
                # Calcula o vetor de reflexão R = 2(N·L)N - L
                reflection_vector = 2 * np.dot(normal, self.light_direction) * normal - self.light_direction
                reflection_vector = reflection_vector / np.linalg.norm(reflection_vector)
                
                # Calcula o ângulo entre o vetor de reflexão e a direção de visualização
                cos_alpha = np.dot(reflection_vector, view_direction)
                cos_alpha = max(0, cos_alpha)  # Não permite valores negativos
                
                # Componente especular com expoente de brilho
                specular_intensity = self.specular_light * (cos_alpha ** self.shininess)
                
                # Intensidade total
                total_intensity = ambient_intensity + diffuse_intensity + specular_intensity
                total_intensity = min(1.0, total_intensity)  # Limita a 1.0
                
                # Para superfícies especulares, mantém alta saturação
                saturation = 0.8
                
                # Converte HSV para RGB
                rgb = colorsys.hsv_to_rgb(self.hue / 360.0, saturation, total_intensity)
                
                # Aplica a cor da luz amarelada
                rgb = np.array(rgb) * self.light_color
                rgb = np.clip(rgb, 0, 1)  # Limita valores entre 0 e 1
                
                colors.append(rgb)
        
        return colors
    
    def get_face_centers(self):
        """Retorna o centro de cada face para ordenação no algoritmo do pintor"""
        centers = []
        for face in self.faces:
            face_vertices = [self.vertices[idx] + self.position for idx in face]
            center = np.mean(face_vertices, axis=0)
            centers.append(center)
        return np.array(centers)
    
    def get_face_depth(self, view_direction):
        """Calcula a profundidade de cada face em relação à direção de visualização"""
        centers = self.get_face_centers()
        depths = np.dot(centers, view_direction)
        return depths

def create_torus_with_specular_top(R=2, r=1, n_u=20, n_v=20, position=(0, 0, 0), hue=240):
    """Cria um toro onde apenas a parte superior tem material especular"""
    vertices = []
    for i in range(n_u):
        u = 2 * np.pi * i / n_u
        for j in range(n_v):
            v = 2 * np.pi * j / n_v
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)
            vertices.append((x, y, z))
    
    # Função para índice linear dos vértices
    def idx(i, j):
        return (i % n_u) * n_v + (j % n_v)
    
    # Geração das faces
    faces = []
    for i in range(n_u):
        for j in range(n_v):
            a = idx(i, j)
            b = idx(i + 1, j)
            c = idx(i + 1, j + 1)
            d = idx(i, j + 1)
            faces.append([a, b, c, d])
    
    # Cria o toro base
    torus = Object3D(vertices, faces, position, hue, "diffuse")
    
    # Identifica as faces da parte superior (z > 0) e as torna especulares
    for i, face in enumerate(faces):
        # Calcula o centro da face
        face_vertices = [vertices[idx] for idx in face]
        center_z = sum(v[2] for v in face_vertices) / len(face_vertices)
        
        # Se a face está na parte superior (z > 0), torna especular
        if center_z > 0:
            torus.face_materials = getattr(torus, 'face_materials', {})
            torus.face_materials[i] = "specular"
    
    return torus

def create_cube(size=1.0, position=(0, 0, 0), hue=240):
    """Cria um cubo com os parâmetros especificados"""
    # Vértices do cubo
    vertices = [
        (-size/2, -size/2, -size/2), (size/2, -size/2, -size/2),
        (size/2, size/2, -size/2), (-size/2, size/2, -size/2),
        (-size/2, -size/2, size/2), (size/2, -size/2, size/2),
        (size/2, size/2, size/2), (-size/2, size/2, size/2)
    ]
    
    # Faces do cubo (6 faces, cada uma com 4 vértices)
    faces = [
        [0, 1, 2, 3],  # Face traseira
        [4, 7, 6, 5],  # Face frontal
        [0, 4, 5, 1],  # Face inferior
        [2, 6, 7, 3],  # Face superior
        [0, 3, 7, 4],  # Face esquerda
        [1, 5, 6, 2]   # Face direita
    ]
    
    return Object3D(vertices, faces, position, hue, "diffuse")

def create_sphere(radius=1.0, n_phi=20, n_theta=20, position=(0, 0, 0), hue=240):
    """
    Cria uma esfera usando coordenadas esféricas (seção 3.2.11)
    Parâmetros:
    - radius: raio da esfera
    - n_phi: número de divisões em latitude (φ)
    - n_theta: número de divisões em longitude (θ)
    - position: posição central da esfera
    - hue: cor base da esfera
    """
    vertices = []
    
    # Gera vértices usando coordenadas esféricas
    for i in range(n_phi + 1):
        phi = np.pi * i / n_phi  # Latitude: 0 a π
        for j in range(n_theta + 1):
            theta = 2 * np.pi * j / n_theta  # Longitude: 0 a 2π
            
            # Conversão para coordenadas cartesianas
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            
            vertices.append((x, y, z))
    
    # Gera faces (quadriláteros)
    faces = []
    for i in range(n_phi):
        for j in range(n_theta):
            # Índices dos vértices do quadrilátero
            v1 = i * (n_theta + 1) + j
            v2 = i * (n_theta + 1) + (j + 1)
            v3 = (i + 1) * (n_theta + 1) + (j + 1)
            v4 = (i + 1) * (n_theta + 1) + j
            
            faces.append([v1, v2, v3, v4])
    
    return Object3D(vertices, faces, position, hue, "specular")

def apply_transformations(vertices, transformacoes):
    """Aplica transformações aos vértices"""
    transformed_vertices = vertices.copy()
    
    for transformacao in transformacoes:
        tipo = transformacao[0]
        
        if tipo == "translate":
            x, y, z = transformacao[1], transformacao[2], transformacao[3]
            for i in range(len(transformed_vertices)):
                transformed_vertices[i] = (
                    transformed_vertices[i][0] + x,
                    transformed_vertices[i][1] + y,
                    transformed_vertices[i][2] + z
                )
        
        elif tipo == "rotate":
            angulo, x, y, z = transformacao[1], transformacao[2], transformacao[3], transformacao[4]
            # Converte ângulo para radianos
            angulo_rad = np.radians(angulo)
            
            # Matriz de rotação em torno do eixo Z (simplificado)
            cos_a = np.cos(angulo_rad)
            sin_a = np.sin(angulo_rad)
            
            for i in range(len(transformed_vertices)):
                vx, vy, vz = transformed_vertices[i]
                # Rotação em torno do eixo Z
                new_x = vx * cos_a - vy * sin_a
                new_y = vx * sin_a + vy * cos_a
                transformed_vertices[i] = (new_x, new_y, vz)
        
        elif tipo == "scale":
            sx, sy, sz = transformacao[1], transformacao[2], transformacao[3]
            for i in range(len(transformed_vertices)):
                transformed_vertices[i] = (
                    transformed_vertices[i][0] * sx,
                    transformed_vertices[i][1] * sy,
                    transformed_vertices[i][2] * sz
                )
    
    return transformed_vertices

def create_butterfly():
    """Cria uma borboleta usando cubos para todas as partes (asas planas)"""
    borboleta = {
        "partes": [
            {"tipo": "cubo", "escala": (0.2, 1.5, 0.2), "transformacoes": [("translate", 0, 0.75, 0)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.3, 0.3, 0.3), "transformacoes": [("translate", 0, 1.6, 0)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.04, 0.4, 0.04), "transformacoes": [("translate", 0.08, 1.8, 0), ("rotate", -50, 0, 0, 1)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.04, 0.4, 0.04), "transformacoes": [("translate", -0.08, 1.8, 0), ("rotate", 50, 0, 0, 1)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.9, 0.7, 0.02), "transformacoes": [("translate", -0.5, 0.9, 0)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.9, 0.7, 0.02), "transformacoes": [("translate", 0.5, 0.9, 0)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.7, 0.5, 0.02), "transformacoes": [("translate", -0.45, 0.3, 0)], "material": "diffuse"},
            {"tipo": "cubo", "escala": (0.7, 0.5, 0.02), "transformacoes": [("translate", 0.45, 0.3, 0)], "material": "diffuse"}
        ]
    }
    
    objects = []
    cores = [300, 280, 260, 240, 220, 200, 180, 160]  # Tons de roxo/azul
    for i, parte in enumerate(borboleta["partes"]):
        cubo_base = create_cube(size=1.0, hue=cores[i])
        vertices_escalados = apply_transformations(
            cubo_base.vertices, 
            [("scale", parte["escala"][0], parte["escala"][1], parte["escala"][2])]
        )
        vertices_finais = apply_transformations(vertices_escalados, parte["transformacoes"])
        objeto = Object3D(vertices_finais, cubo_base.faces, (0, 0, 0), cores[i], parte["material"])
        objects.append(objeto)
    return objects

# Criação dos objetos
torus = create_torus_with_specular_top(position=(-2, 0, 0), hue=240)  # Toro com parte superior especular
borboleta_objects = create_butterfly()                                # Borboleta no centro

# Ajusta a posição da borboleta para ficar em cima do toro
for obj in borboleta_objects:
    obj.position = np.array([-2, 0, 2])  # Posiciona em cima do toro

objects = [torus] + borboleta_objects  # Toro e borboleta

# Ângulos de rotação iniciais
elevation = 30
azimuth = 45

# Variáveis para controle do mouse
is_dragging = False
last_mouse_pos = None

def on_mouse_press(event):
    global is_dragging, last_mouse_pos
    if event.inaxes == ax:
        is_dragging = True
        last_mouse_pos = (event.xdata, event.ydata)

def on_mouse_release(event):
    global is_dragging
    is_dragging = False

def on_mouse_move(event):
    global elevation, azimuth, last_mouse_pos
    if is_dragging and event.inaxes == ax and last_mouse_pos is not None:
        dx = event.xdata - last_mouse_pos[0]
        dy = event.ydata - last_mouse_pos[1]
        
        azimuth += dx * 2
        elevation += dy * 2
        
        elevation = max(-90, min(90, elevation))
        azimuth = azimuth % 360
        
        update_view()
        last_mouse_pos = (event.xdata, event.ydata)

def update_view():
    ax.view_init(elev=elevation, azim=azimuth)
    plt.draw()

def painter_algorithm(objects, view_direction):
    """
    Implementa o algoritmo do pintor (seção 5.3.3.1)
    Ordena as faces de todos os objetos por profundidade (mais distante primeiro)
    """
    all_faces = []
    
    for obj_idx, obj in enumerate(objects):
        # Calcula profundidade de cada face do objeto
        depths = obj.get_face_depth(view_direction)
        
        for face_idx, face in enumerate(obj.faces):
            all_faces.append({
                'object_idx': obj_idx,
                'face_idx': face_idx,
                'face': face,
                'depth': depths[face_idx],
                'normal': obj.face_normals[face_idx]
            })
    
    # Ordena por profundidade (mais distante primeiro)
    all_faces.sort(key=lambda x: x['depth'])
    
    return all_faces

def render_scene():
    """Renderiza a cena uma vez (sem animação)"""
    ax.clear()
    
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
    ax.set_xlim(-4, 1)  # Ajustado para mostrar toro e borboleta
    ax.set_ylim(-3, 3)  # Ajustado para mostrar toro e borboleta
    ax.set_zlim(-2, 4)  # Ajustado para mostrar toro e borboleta
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Cena 3D com Superfície Curva no Toro e Sombreamento de Phong\nParte Superior do Toro Especular Polida - Arraste o mouse para rotacionar")
    
    # Define o ângulo de visualização
    ax.view_init(elev=elevation, azim=azimuth)

# Configuração da figura
plt.ion()
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Conecta os eventos do mouse
fig.canvas.mpl_connect('button_press_event', on_mouse_press)
fig.canvas.mpl_connect('button_release_event', on_mouse_release)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Renderiza a cena inicial
render_scene()

# Instruções para o usuário
print("=== CENA 3D COM SUPERFÍCIE CURVA NO TORO E SOMBREAMENTO DE PHONG ===")
print("• Toro azul com parte superior especular (superfície curva polida)")
print("• Borboleta com asas planas (superfícies difusas)")
print("• Sombreamento de Phong com reflexão especular na parte superior do toro")
print("• Luz amarelada conforme tabela 5.1")
print("• Algoritmo do pintor para resolver oclusão")
print("• Arraste o mouse para rotacionar a cena")
print("• Pressione 'q' para sair")

# Estatísticas dos objetos
print(f"\n=== ESTATÍSTICAS DOS OBJETOS ===")
print(f"Toro: {len(torus.vertices)} vértices, {len(torus.faces)} faces")
print(f"  - Partes difusas: faces inferiores")
print(f"  - Partes especulares: faces superiores")
print(f"Borboleta: {sum(len(obj.vertices) for obj in borboleta_objects)} vértices, {sum(len(obj.faces) for obj in borboleta_objects)} faces")
print(f"Total de partes da borboleta: {len(borboleta_objects)}")
print("\nPartes da borboleta:")
partes_nomes = ["Corpo", "Cabeça", "Antena Esq", "Antena Dir", "Asa Sup Esq", "Asa Sup Dir", "Asa Inf Esq", "Asa Inf Dir"]
for i, obj in enumerate(borboleta_objects):
    print(f"  {partes_nomes[i]}: {len(obj.vertices)} vértices, {len(obj.faces)} faces - Difuso")

print(f"\n=== PARÂMETROS DE ILUMINAÇÃO ===")
print(f"Luz amarelada (RGB): {torus.light_color}")
print(f"Expoente de brilho (n): {torus.shininess}")
print(f"Intensidade especular: {torus.specular_light}")

plt.show(block=True)

"""
MELHORIAS IMPLEMENTADAS PARA O TRABALHO 1:

1. SUPERFÍCIES CURVAS (Seção 3.2.11):
   - Transformação das asas da borboleta em esferas
   - Uso de coordenadas esféricas para geração de vértices
   - Parametrização em φ (latitude) e θ (longitude)
   - Conversão para coordenadas cartesianas: x = r*sin(φ)*cos(θ), y = r*sin(φ)*sin(θ), z = r*cos(φ)

2. SOMBREAMENTO DE PHONG (Seção 5.4.4.3):
   - Implementação do modelo completo: I = Ia + Id*cos(θ) + Is*(cos(α))^n
   - Cálculo do vetor de reflexão: R = 2(N·L)N - L
   - Expoente de brilho n = 32 para superfícies polidas
   - Componente especular com intensidade Is = 0.8

3. LUZ AMARELADA (Tabela 5.1):
   - Implementação de luz colorida com RGB = (1.0, 0.9, 0.7)
   - Aplicação da cor da luz nas superfícies especulares
   - Mantém superfícies difusas com iluminação original

4. DIFERENCIAÇÃO DE MATERIAIS:
   - Superfícies planas (corpo, antenas): material difuso
   - Superfícies curvas (asas): material especular polido
   - Toro: mantém material difuso original

5. CONCEITOS TEÓRICOS APLICADOS:
   - Modelagem de superfícies paramétricas
   - Reflexão especular e difusa
   - Modelo de iluminação de Phong
   - Coordenadas esféricas e cartesianas
   - Algoritmo do pintor para oclusão
   - Controles de câmera interativos
""" 