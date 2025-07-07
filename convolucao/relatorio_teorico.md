# Relatório Teórico: Superfícies Curvas e Sombreamento de Phong

## 1. Introdução

Este relatório documenta a implementação de superfícies curvas e sombreamento de Phong no contexto de computação gráfica, conforme solicitado no Trabalho 1. A implementação transforma as asas de uma borboleta 3D de superfícies planas para superfícies curvas (esferas) e aplica o modelo de iluminação de Phong com reflexão especular.

## 2. Modelagem de Superfícies Curvas

### 2.1 Fundamentos Teóricos (Seção 3.2.11)

As superfícies curvas foram implementadas usando **coordenadas esféricas**, que permitem representar pontos em 3D através de três parâmetros:

- **r (raio)**: Distância do ponto à origem
- **φ (phi)**: Ângulo de latitude (0 ≤ φ ≤ π)
- **θ (theta)**: Ângulo de longitude (0 ≤ θ ≤ 2π)

### 2.2 Conversão para Coordenadas Cartesianas

A conversão de coordenadas esféricas para cartesianas segue as equações:

```
x = r * sin(φ) * cos(θ)
y = r * sin(φ) * sin(θ)
z = r * cos(φ)
```

### 2.3 Implementação Computacional

```python
def create_sphere(radius=1.0, n_phi=20, n_theta=20, position=(0, 0, 0), hue=240):
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
```

### 2.4 Geração de Faces

As faces são geradas como quadriláteros conectando vértices adjacentes:

```python
# Gera faces (quadriláteros)
faces = []
for i in range(n_phi):
    for j in range(n_theta):
        v1 = i * (n_theta + 1) + j
        v2 = i * (n_theta + 1) + (j + 1)
        v3 = (i + 1) * (n_theta + 1) + (j + 1)
        v4 = (i + 1) * (n_theta + 1) + j
        
        faces.append([v1, v2, v3, v4])
```

## 3. Sombreamento de Phong

### 3.1 Modelo Teórico (Seção 5.4.4.3)

O modelo de iluminação de Phong combina três componentes:

1. **Componente Ambiente (Ia)**: Iluminação uniforme de fundo
2. **Componente Difusa (Id)**: Reflexão difusa baseada no ângulo entre normal e direção da luz
3. **Componente Especular (Is)**: Reflexão especular baseada no ângulo entre vetor de reflexão e direção de visualização

### 3.2 Equação do Modelo de Phong

```
I = Ia + Id * cos(θ) + Is * (cos(α))^n
```

Onde:
- **Ia**: Intensidade da luz ambiente
- **Id**: Intensidade da luz difusa
- **Is**: Intensidade da luz especular
- **θ**: Ângulo entre a normal da superfície e a direção da luz
- **α**: Ângulo entre o vetor de reflexão e a direção de visualização
- **n**: Expoente de brilho (shininess)

### 3.3 Cálculo do Vetor de Reflexão

O vetor de reflexão é calculado usando a fórmula:

```
R = 2(N·L)N - L
```

Onde:
- **N**: Vetor normal da superfície
- **L**: Vetor direção da luz
- **R**: Vetor de reflexão

### 3.4 Implementação Computacional

```python
def get_illuminated_colors(self, view_direction):
    colors = []
    
    for i, face in enumerate(self.faces):
        normal = self.face_normals[i]
        
        # Componente ambiente
        ambient_intensity = self.ambient_light
        
        # Componente difusa
        cos_angle = np.dot(normal, self.light_direction)
        cos_angle = max(0, cos_angle)
        diffuse_intensity = self.diffuse_light * cos_angle
        
        # Componente especular
        reflection_vector = 2 * np.dot(normal, self.light_direction) * normal - self.light_direction
        reflection_vector = reflection_vector / np.linalg.norm(reflection_vector)
        
        cos_alpha = np.dot(reflection_vector, view_direction)
        cos_alpha = max(0, cos_alpha)
        
        specular_intensity = self.specular_light * (cos_alpha ** self.shininess)
        
        # Intensidade total
        total_intensity = ambient_intensity + diffuse_intensity + specular_intensity
```

## 4. Luz Amarelada (Tabela 5.1)

### 4.1 Implementação da Luz Colorida

A luz amarelada foi implementada usando valores RGB aproximados:

```python
self.light_color = np.array([1.0, 0.9, 0.7])  # Luz amarelada
```

### 4.2 Aplicação da Cor da Luz

A cor da luz é aplicada multiplicando os componentes RGB:

```python
# Aplica a cor da luz amarelada
rgb = np.array(rgb) * self.light_color
rgb = np.clip(rgb, 0, 1)  # Limita valores entre 0 e 1
```

## 5. Diferenciação de Materiais

### 5.1 Superfícies Difusas

- **Corpo, cabeça e antenas da borboleta**
- **Toro base**
- Apenas componentes ambiente e difusa
- Aparência fosca/mate

### 5.2 Superfícies Especulares

- **Asas da borboleta (esferas)**
- Componentes ambiente, difusa e especular
- Expoente de brilho n = 32 (superfícies polidas)
- Aparência brilhante/reflexiva

## 6. Parâmetros de Implementação

### 6.1 Superfícies Curvas
- **Asas superiores**: Raio = 0.6, n_phi = 15, n_theta = 15
- **Asas inferiores**: Raio = 0.5, n_phi = 12, n_theta = 12
- **Escala**: Aplicada para criar formato de asa

### 6.2 Iluminação
- **Luz ambiente**: 0.3
- **Luz difusa**: 0.7
- **Luz especular**: 0.8
- **Expoente de brilho**: 32
- **Luz amarelada**: RGB(1.0, 0.9, 0.7)

## 7. Resultados e Visualização

### 7.1 Estatísticas dos Objetos
- **Toro**: 400 vértices, 400 faces
- **Borboleta**: 882 vértices, 762 faces
- **Asas especulares**: 850 vértices, 738 faces
- **Partes difusas**: 32 vértices, 24 faces

### 7.2 Imagens Geradas
Foram geradas 7 imagens em diferentes ângulos:
- Vista frontal (30°, 45°)
- Vista lateral direita (30°, 135°)
- Vista traseira (30°, 225°)
- Vista lateral esquerda (30°, 315°)
- Vista superior (60°, 45°)
- Vista inferior (0°, 45°)
- Vista diagonal (45°, 90°)

## 8. Conclusões

A implementação demonstra com sucesso:

1. **Modelagem de superfícies curvas** usando coordenadas esféricas
2. **Sombreamento de Phong** com reflexão especular
3. **Luz colorida** aplicada corretamente
4. **Diferenciação de materiais** entre superfícies difusas e especulares
5. **Algoritmo do pintor** para resolução de oclusão

O resultado visual mostra claramente a diferença entre as superfícies planas (corpo, antenas) com aparência fosca e as superfícies curvas (asas) com aparência polida e reflexiva, iluminadas pela luz amarelada conforme especificado.

## 9. Sugestões para Compartilhamento

Para que a implementação e resultados possam ser vistos por todos da turma, sugiro:

1. **Compartilhamento do código**: Disponibilizar os arquivos Python
2. **Imagens geradas**: Incluir as 7 imagens em diferentes ângulos
3. **Execução interativa**: Permitir que outros executem o código
4. **Documentação**: Este relatório teórico
5. **Demonstração**: Apresentação com visualização interativa

### 9.1 Requisitos para Execução
```python
# Dependências necessárias
numpy
matplotlib
mpl_toolkits.mplot3d
```

### 9.2 Comandos de Execução
```bash
# Execução interativa
python comp_graf_curved_surfaces.py

# Geração de imagens
python generate_images.py
``` 