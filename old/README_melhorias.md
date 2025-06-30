# Melhorias Implementadas - Cena 3D Realista

## Visão Geral

Este projeto implementa uma cena 3D realista com múltiplos objetos, iluminação avançada e algoritmos de oclusão, seguindo as especificações do trabalho de Computação Gráfica.

## Arquivos Principais

### 1. `comp_graf.py` - Algoritmo do Pintor
- Implementa o **algoritmo do pintor** (seção 5.3.3.1)
- Renderiza faces do mais distante para o mais próximo
- Toro azul e cubo verde

### 2. `comp_graf_z_buffer.py` - Algoritmo Z-Buffer
- Implementa o **algoritmo Z-buffer** (seção 5.3.3.2)
- Renderiza faces do mais próximo para o mais distante
- Toro azul, cubo verde e esfera vermelha

## Funcionalidades Implementadas

### 1. Iluminação Realista (Seção 5.4.3)

#### Características:
- **Hue (H) fixo** para cada objeto (aparência fosca)
- **Variação de intensidade (I)** baseada no ângulo de iluminação
- **Variação de saturação (S)** baseada na intensidade
- **Luz ambiente (Ia = 0.3)** conforme seção 5.4.1
- **Luz difusa (Id = 0.7)** para iluminação direcional

#### Modelo de Iluminação:
```
I = Ia + Id * cos(θ)
```
Onde:
- `Ia` = luz ambiente (0.3)
- `Id` = luz difusa (0.7)
- `θ` = ângulo entre a normal da face e a direção da luz

### 2. Múltiplos Objetos 3D

#### Objetos Implementados:
- **Toro**: Gerado por coordenadas paramétricas
- **Cubo**: 6 faces quadrilaterais
- **Esfera**: Malha triangular (apenas no Z-buffer)

#### Posicionamento:
- Objetos posicionados no mesmo campo visual
- Criação de oclusão natural entre objetos
- Suporte para posicionamento relativo

### 3. Algoritmos de Oclusão

#### Algoritmo do Pintor (comp_graf.py):
- Ordenação de faces por profundidade
- Renderização do mais distante para o mais próximo
- Resolução correta de oclusão sem canal alfa

#### Algoritmo Z-Buffer (comp_graf_z_buffer.py):
- Ordenação de faces por profundidade
- Renderização do mais próximo para o mais distante
- Simulação do comportamento do Z-buffer

### 4. Interatividade

#### Controles:
- **Mouse**: Arraste para rotacionar a cena
- **Ângulos**: Elevação (-90° a 90°) e Azimute (0° a 360°)
- **Visualização**: Projeção 3D interativa

## Conceitos de Computação Gráfica Aplicados

### 1. Modelagem 3D
- **Coordenadas paramétricas** para toro
- **Malhas de polígonos** (faces quadrilaterais e triangulares)
- **Cálculo de normais** de faces

### 2. Iluminação
- **Modelo de Phong** simplificado
- **Luz ambiente e difusa**
- **Cálculo de ângulos** de incidência

### 3. Visualização
- **Projeção 3D** com matplotlib
- **Controles de câmera** interativos
- **Transformações** de coordenadas

### 4. Algoritmos de Renderização
- **Ordenação de profundidade**
- **Resolução de oclusão**
- **Renderização por faces**

## Como Executar

### Pré-requisitos:
```bash
pip install numpy matplotlib
```

### Execução:
```bash
# Algoritmo do Pintor
python comp_graf.py

# Algoritmo Z-Buffer
python comp_graf_z_buffer.py
```

## Controles

1. **Clique e arraste** o mouse para rotacionar a cena
2. **Visualize** a oclusão sendo resolvida corretamente
3. **Observe** as variações de iluminação nas faces
4. **Pressione 'q'** para sair

## Diferenças Entre os Algoritmos

### Algoritmo do Pintor:
- ✅ Simples de implementar
- ✅ Funciona bem para cenas simples
- ❌ Pode ter problemas com faces que se intersectam
- ❌ Ordenação pode ser complexa

### Algoritmo Z-Buffer:
- ✅ Resolve todos os casos de oclusão
- ✅ Mais robusto para cenas complexas
- ❌ Requer mais memória (buffer de profundidade)
- ❌ Mais complexo de implementar completamente

## Estrutura do Código

### Classe Object3D:
```python
class Object3D:
    def __init__(self, vertices, faces, position, hue)
    def _calculate_face_normals(self)
    def get_illuminated_colors(self, view_direction)
    def get_face_depth(self, view_direction)
```

### Funções de Criação:
```python
def create_torus(R, r, n_u, n_v, position, hue)
def create_cube(size, position, hue)
def create_sphere(radius, n_phi, n_theta, position, hue)
```

### Algoritmos de Oclusão:
```python
def painter_algorithm(objects, view_direction)
def z_buffer_algorithm(objects, view_direction)
```

## Resultados Esperados

1. **Objetos foscos** com mesmo hue por objeto
2. **Iluminação realista** com variações de intensidade
3. **Oclusão correta** entre objetos
4. **Interatividade** fluida
5. **Performance** adequada para visualização

## Próximos Passos

Para expandir o projeto, considere:
- Implementar Z-buffer completo com buffer de profundidade
- Adicionar mais tipos de iluminação (especular, sombras)
- Suporte para texturas
- Otimizações de performance
- Mais primitivas 3D 