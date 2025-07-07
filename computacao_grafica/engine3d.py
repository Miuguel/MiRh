import numpy as np
from PIL import Image
import math

class Vector3:
    """Classe para representar vetores 3D"""
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length > 0:
            return Vector3(self.x/length, self.y/length, self.z/length)
        return Vector3(0, 0, 0)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

class Triangle:
    """Classe para representar um triângulo 3D"""
    def __init__(self, v1, v2, v3, normal=None, material="diffuse", hue=240):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = normal if normal else self.calculate_normal()
        self.material = material
        self.hue = hue
    
    def calculate_normal(self):
        """Calcula a normal do triângulo"""
        edge1 = self.v2 - self.v1
        edge2 = self.v3 - self.v1
        normal = edge1.cross(edge2)
        return normal.normalize()

class Camera:
    """Classe para representar uma câmera 3D"""
    def __init__(self, position, target, up, fov=60, aspect_ratio=1.0):
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        # Calcula os vetores da câmera
        self.forward = (target - position).normalize()
        self.right = self.forward.cross(up).normalize()
        self.up_cam = self.right.cross(self.forward).normalize()
    
    def get_view_matrix(self):
        """Retorna a matriz de visualização"""
        # Matriz de translação
        translation = np.array([
            [1, 0, 0, -self.position.x],
            [0, 1, 0, -self.position.y],
            [0, 0, 1, -self.position.z],
            [0, 0, 0, 1]
        ])
        
        # Matriz de rotação
        rotation = np.array([
            [self.right.x, self.right.y, self.right.z, 0],
            [self.up_cam.x, self.up_cam.y, self.up_cam.z, 0],
            [-self.forward.x, -self.forward.y, -self.forward.z, 0],
            [0, 0, 0, 1]
        ])
        
        return rotation @ translation
    
    def get_projection_matrix(self, near=0.1, far=100.0):
        """Retorna a matriz de projeção"""
        f = 1.0 / math.tan(math.radians(self.fov) / 2.0)
        
        return np.array([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ])

class Renderer3D:
    """Engine 3D completa"""
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.z_buffer = np.full((height, width), float('inf'))
        self.frame_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Parâmetros de iluminação melhorados
        self.light_direction = Vector3(0, 0, 1).normalize()  # Luz vindo de cima
        self.light_color = np.array([1.0, 1.0, 1.0])  # Luz branca pura
        self.ambient_light = 0.3  # Luz ambiente moderada
        self.diffuse_light = 0.7  # Luz difusa mais forte
        self.specular_light = 0.5  # Especular moderado
        self.shininess = 16  # Brilho moderado
    
    def clear_buffers(self):
        """Limpa os buffers de renderização"""
        self.z_buffer.fill(float('inf'))
        self.frame_buffer.fill(0)
    
    def project_vertex(self, vertex, view_matrix, proj_matrix):
        """Projeta um vértice 3D para 2D"""
        # Converte para coordenadas homogêneas
        v = np.array([vertex.x, vertex.y, vertex.z, 1.0])
        
        # Aplica transformações
        v = view_matrix @ v
        v = proj_matrix @ v
        
        # Divisão perspectiva
        if v[3] != 0:
            v = v / v[3]
        
        # Converte para coordenadas de tela
        x = int((v[0] + 1) * self.width / 2)
        y = int((1 - v[1]) * self.height / 2)
        z = v[2]
        
        return x, y, z
    
    def phong_shading(self, normal, view_direction, material_type="diffuse", specular_factor=None):
        """Calcula o sombreamento de Phong com gradiente suave"""
        if material_type == "diffuse" or specular_factor is None:
            # Modelo difuso simples
            cos_angle = max(0, normal.dot(self.light_direction))
            intensity = self.ambient_light + self.diffuse_light * cos_angle
            return np.array([intensity, intensity, intensity])
        
        elif material_type == "specular":
            # Modelo de Phong com gradiente suave
            cos_angle = max(0, normal.dot(self.light_direction))
            
            # Componente ambiente
            ambient_intensity = self.ambient_light
            
            # Componente difusa
            diffuse_intensity = self.diffuse_light * cos_angle
            
            # Componente especular com gradiente
            reflection_vector = normal * (2 * normal.dot(self.light_direction)) - self.light_direction
            reflection_vector = reflection_vector.normalize()
            
            cos_alpha = max(0, reflection_vector.dot(view_direction))
            # Usa o fator de especularidade para suavizar o gradiente
            specular_intensity = self.specular_light * (cos_alpha ** self.shininess) * specular_factor
            
            # Intensidade total
            total_intensity = ambient_intensity + diffuse_intensity + specular_intensity
            total_intensity = min(1.0, total_intensity)
            
            # Aplica cor da luz
            color = np.array([total_intensity, total_intensity, total_intensity]) * self.light_color
            return np.clip(color, 0, 1)
    
    def rasterize_triangle(self, triangle, view_direction, hue=None):
        """Rasteriza um triângulo com sombreamento por pixel (Phong shading)"""
        # Projeta os vértices
        x1, y1, z1 = self.project_vertex(triangle.v1, self.view_matrix, self.proj_matrix)
        x2, y2, z2 = self.project_vertex(triangle.v2, self.view_matrix, self.proj_matrix)
        x3, y3, z3 = self.project_vertex(triangle.v3, self.view_matrix, self.proj_matrix)
        
        # Calcula bounding box
        min_x = max(0, min(x1, x2, x3))
        max_x = min(self.width - 1, max(x1, x2, x3))
        min_y = max(0, min(y1, y2, y3))
        max_y = min(self.height - 1, max(y1, y2, y3))
        
        if min_x > max_x or min_y > max_y:
            return
        
        # Usa o hue do triângulo se não for passado
        if hue is None:
            hue = getattr(triangle, 'hue', 240)
        # Converte HSV para RGB
        saturation = 0.8 if triangle.material == "specular" else 1.0
        rgb = self.hsv_to_rgb(hue/360.0, saturation, 1.0)
        
        # Rasterização com sombreamento por pixel
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                # Teste de ponto no triângulo (barycentric coordinates)
                if self.point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
                    # Interpolação de profundidade
                    z = self.interpolate_z(x, y, x1, y1, z1, x2, y2, z2, x3, y3, z3)
                    
                    # Teste de Z-buffer
                    if z < self.z_buffer[y, x]:
                        # Interpolação de normal por pixel (Phong shading)
                        barycentric = self.get_barycentric_coords(x, y, x1, y1, x2, y2, x3, y3)
                        if barycentric is not None:
                            w1, w2, w3 = barycentric
                            
                            # Interpola normal por pixel
                            normal1 = self.calculate_vertex_normal(triangle.v1, triangle.normal)
                            normal2 = self.calculate_vertex_normal(triangle.v2, triangle.normal)
                            normal3 = self.calculate_vertex_normal(triangle.v3, triangle.normal)
                            
                            interpolated_normal = (w1 * normal1 + w2 * normal2 + w3 * normal3).normalize()
                            
                            # Calcula sombreamento por pixel
                            shading = self.phong_shading(interpolated_normal, view_direction, triangle.material, getattr(triangle, 'specular_factor', None))
                            
                            # Aplica suavização para eliminar bandas
                            shading = self.apply_smooth_shading(shading)
                            
                            # Aplica sombreamento
                            final_rgb = rgb * shading * 255
                            
                            self.z_buffer[y, x] = z
                            self.frame_buffer[y, x] = final_rgb.astype(np.uint8)
    
    def calculate_vertex_normal(self, vertex, face_normal):
        """Calcula normal por vértice para sombreamento mais suave"""
        # Para o toro, cria variação baseada na posição esférica
        if hasattr(vertex, 'is_torus_vertex'):
            # Variação mais suave para o toro
            variation_x = math.sin(vertex.x * 2) * math.cos(vertex.y * 2) * 0.05
            variation_y = math.cos(vertex.x * 2) * math.sin(vertex.z * 2) * 0.05
            variation_z = math.sin(vertex.y * 2) * math.cos(vertex.z * 2) * 0.05
        else:
            # Variação para outros objetos
            variation_x = math.sin(vertex.x * 3) * math.cos(vertex.y * 2) * 0.1
            variation_y = math.cos(vertex.x * 2) * math.sin(vertex.z * 3) * 0.1
            variation_z = math.sin(vertex.y * 2.5) * math.cos(vertex.z * 2) * 0.1
        
        variation = Vector3(variation_x, variation_y, variation_z)
        normal = face_normal + variation
        return normal.normalize()
    
    def get_barycentric_coords(self, x, y, x1, y1, x2, y2, x3, y3):
        """Calcula coordenadas baricêntricas"""
        denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if abs(denom) < 1e-10:
            return None
        
        w1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
        w2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
        w3 = 1 - w1 - w2
        
        return w1, w2, w3
    
    def point_in_triangle(self, x, y, x1, y1, x2, y2, x3, y3):
        """Testa se um ponto está dentro do triângulo"""
        def sign(x1, y1, x2, y2, x3, y3):
            return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
        
        d1 = sign(x, y, x1, y1, x2, y2)
        d2 = sign(x, y, x2, y2, x3, y3)
        d3 = sign(x, y, x3, y3, x1, y1)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    def interpolate_z(self, x, y, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        """Interpola a profundidade Z"""
        # Barycentric coordinates
        denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if denom == 0:
            return z1
        
        w1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denom
        w2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denom
        w3 = 1 - w1 - w2
        
        return w1 * z1 + w2 * z2 + w3 * z3
    
    def hsv_to_rgb(self, h, s, v):
        """Converte HSV para RGB"""
        if s == 0:
            return np.array([v, v, v])
        
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i = i % 6
        if i == 0:
            return np.array([v, t, p])
        elif i == 1:
            return np.array([q, v, p])
        elif i == 2:
            return np.array([p, v, t])
        elif i == 3:
            return np.array([p, q, v])
        elif i == 4:
            return np.array([t, p, v])
        else:
            return np.array([v, p, q])
    
    def render_scene(self, triangles, camera):
        """Renderiza a cena completa"""
        self.clear_buffers()
        
        # Calcula matrizes de transformação
        self.view_matrix = camera.get_view_matrix()
        self.proj_matrix = camera.get_projection_matrix()
        
        # Direção de visualização
        view_direction = camera.forward
        
        # Renderiza cada triângulo
        for triangle in triangles:
            self.rasterize_triangle(triangle, view_direction)
    
    def save_image(self, filename):
        """Salva a imagem renderizada"""
        image = Image.fromarray(self.frame_buffer)
        image.save(filename)
        print(f"Imagem salva: {filename}")
    
    def apply_smooth_shading(self, shading):
        """Aplica suavização ao sombreamento para eliminar bandas"""
        # Aplica uma função de suavização para reduzir bandas
        smoothed = np.power(shading, 0.7)  # Gamma correction
        return np.clip(smoothed, 0.1, 1.0)  # Evita valores muito baixos

def create_torus_triangles(R=2, r=1, n_u=20, n_v=20, position=Vector3(0, 0, 0), hue=240):
    """Cria triângulos do toro com iluminação diferenciada e gradiente suave"""
    triangles = []
    vertices = []
    
    # Gera vértices
    for i in range(n_u):
        u = 2 * math.pi * i / n_u
        for j in range(n_v):
            v = 2 * math.pi * j / n_v
            x = (R + r * math.cos(v)) * math.cos(u)
            y = (R + r * math.cos(v)) * math.sin(u)
            z = r * math.sin(v)
            vertex = Vector3(x + position.x, y + position.y, z + position.z)
            vertex.is_torus_vertex = True  # Marca como vértice do toro
            vertex.u_coord = u  # Coordenada U para gradiente
            vertex.v_coord = v  # Coordenada V para gradiente
            vertices.append(vertex)
    
    # Gera triângulos
    for i in range(n_u):
        for j in range(n_v):
            # Índices dos vértices
            a = i * n_v + j
            b = ((i + 1) % n_u) * n_v + j
            c = ((i + 1) % n_u) * n_v + ((j + 1) % n_v)
            d = i * n_v + ((j + 1) % n_v)
            
            # Calcula gradiente suave baseado na posição Z
            center_z = (vertices[a].z + vertices[b].z + vertices[c].z + vertices[d].z) / 4
            # Normaliza a posição Z para criar gradiente suave
            z_normalized = (center_z - position.z) / r  # Normaliza entre -1 e 1
            # Função sigmoid para transição suave
            specular_factor = 1.0 / (1.0 + math.exp(-5 * (z_normalized + 0.2)))
            
            # Determina material com gradiente suave
            material = "specular" if specular_factor > 0.5 else "diffuse"
            
            # Cria dois triângulos
            tri1 = Triangle(vertices[a], vertices[b], vertices[c], material=material, hue=hue)
            tri2 = Triangle(vertices[a], vertices[c], vertices[d], material=material, hue=hue)
            
            # Armazena o fator de especularidade para uso no sombreamento
            tri1.specular_factor = specular_factor
            tri2.specular_factor = specular_factor
            
            triangles.extend([tri1, tri2])
    
    return triangles

def create_cube_triangles(size=1.0, position=Vector3(0, 0, 0), hue=240):
    """Cria triângulos do cubo"""
    triangles = []
    s = size / 2
    
    # Vértices do cubo
    vertices = [
        Vector3(-s, -s, -s), Vector3(s, -s, -s), Vector3(s, s, -s), Vector3(-s, s, -s),
        Vector3(-s, -s, s), Vector3(s, -s, s), Vector3(s, s, s), Vector3(-s, s, s)
    ]
    
    # Aplica posição
    for v in vertices:
        v.x += position.x
        v.y += position.y
        v.z += position.z
    
    # Faces do cubo (cada face = 2 triângulos)
    faces = [
        [0, 1, 2, 3], [4, 7, 6, 5], [0, 4, 5, 1], [2, 6, 7, 3], [0, 3, 7, 4], [1, 5, 6, 2]
    ]
    
    for face in faces:
        # Primeiro triângulo
        tri1 = Triangle(vertices[face[0]], vertices[face[1]], vertices[face[2]], material="diffuse", hue=hue)
        # Segundo triângulo
        tri2 = Triangle(vertices[face[0]], vertices[face[2]], vertices[face[3]], material="diffuse", hue=hue)
        triangles.extend([tri1, tri2])
    
    return triangles

def create_butterfly_triangles():
    """Cria triângulos da borboleta usando apenas paralelepípedos (cubos escalados)"""
    triangles = []
    cores = [300, 280, 260, 240, 220, 200, 180, 160]
    
    # Partes da borboleta: corpo, cabeça, antenas, asas
    partes = [
        {"escala": (0.2, 1.5, 0.2), "pos": Vector3(0, 0.75, 0)},   # Corpo
        {"escala": (0.3, 0.3, 0.3), "pos": Vector3(0, 1.6, 0)},    # Cabeça
        {"escala": (0.04, 0.4, 0.04), "pos": Vector3(0.08, 1.8, 0)}, # Antena direita
        {"escala": (0.04, 0.4, 0.04), "pos": Vector3(-0.08, 1.8, 0)}, # Antena esquerda
        {"escala": (0.9, 0.7, 0.02), "pos": Vector3(-0.5, 0.9, 0)}, # Asa superior esquerda
        {"escala": (0.9, 0.7, 0.02), "pos": Vector3(0.5, 0.9, 0)},  # Asa superior direita
        {"escala": (0.7, 0.5, 0.02), "pos": Vector3(-0.45, 0.3, 0)}, # Asa inferior esquerda
        {"escala": (0.7, 0.5, 0.02), "pos": Vector3(0.45, 0.3, 0)}   # Asa inferior direita
    ]
    
    for i, parte in enumerate(partes):
        cube_tris = create_scaled_cube_triangles(
            scale=parte["escala"],
            position=parte["pos"],
            hue=cores[i]
        )
        triangles.extend(cube_tris)
    
    return triangles

def create_scaled_cube_triangles(scale=(1.0, 1.0, 1.0), position=Vector3(0, 0, 0), hue=240):
    """Cria triângulos de um cubo com escala personalizada"""
    triangles = []
    sx, sy, sz = scale
    
    # Vértices do cubo com escala
    vertices = [
        Vector3(-sx/2, -sy/2, -sz/2), Vector3(sx/2, -sy/2, -sz/2), 
        Vector3(sx/2, sy/2, -sz/2), Vector3(-sx/2, sy/2, -sz/2),
        Vector3(-sx/2, -sy/2, sz/2), Vector3(sx/2, -sy/2, sz/2), 
        Vector3(sx/2, sy/2, sz/2), Vector3(-sx/2, sy/2, sz/2)
    ]
    
    # Aplica posição
    for v in vertices:
        v.x += position.x
        v.y += position.y
        v.z += position.z
    
    # Faces do cubo (cada face = 2 triângulos)
    faces = [
        [0, 1, 2, 3], [4, 7, 6, 5], [0, 4, 5, 1], 
        [2, 6, 7, 3], [0, 3, 7, 4], [1, 5, 6, 2]
    ]
    
    for face in faces:
        # Primeiro triângulo
        tri1 = Triangle(vertices[face[0]], vertices[face[1]], vertices[face[2]], material="diffuse", hue=hue)
        # Segundo triângulo
        tri2 = Triangle(vertices[face[0]], vertices[face[2]], vertices[face[3]], material="diffuse", hue=hue)
        triangles.extend([tri1, tri2])
    
    return triangles

def main():
    """Função principal"""
    print("=== ENGINE 3D - RENDERIZAÇÃO SEM MATPLOTLIB ===")
    
    # Cria renderer
    renderer = Renderer3D(width=800, height=600)
    
    # Cria câmera focada na cena
    camera = Camera(
        position=Vector3(6, 6, 4),
        target=Vector3(0.5, 0, 1),  # Olha para o centro da cena
        up=Vector3(0, 0, 1),
        fov=50,  # Campo de visão um pouco menor
        aspect_ratio=800/600
    )
    
    # Cria objetos
    torus_triangles = create_torus_triangles(position=Vector3(0, 0, 0), hue=240)
    butterfly_triangles = create_butterfly_triangles()
    
    # Posiciona a borboleta repousando no toro
    for tri in butterfly_triangles:
        tri.v1.z += 1.0  # Posiciona no topo do toro
        tri.v2.z += 1.0
        tri.v3.z += 1.0
        # Centraliza a borboleta
        tri.v1.x += 0.5
        tri.v2.x += 0.5
        tri.v3.x += 0.5
    
    all_triangles = torus_triangles + butterfly_triangles
    
    # Renderiza cena
    renderer.render_scene(all_triangles, camera)
    
    # Salva imagem
    renderer.save_image("engine3d_render.png")
    
    print("Renderização concluída!")

if __name__ == "__main__":
    main() 