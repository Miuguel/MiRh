# Trabalho 1: Superfícies Curvas e Sombreamento de Phong

## Resumo do Trabalho

Este trabalho implementa as melhorias solicitadas no código original de computação gráfica, transformando as asas de uma borboleta 3D de superfícies planas para superfícies curvas (esferas) e aplicando o modelo de iluminação de Phong com reflexão especular e luz amarelada.

## Arquivos do Projeto

### Código Principal
- **`comp_graf_curved_surfaces.py`**: Implementação principal com superfícies curvas e sombreamento de Phong
- **`generate_images.py`**: Script para gerar imagens estáticas em diferentes ângulos
- **`comp_graf.py`**: Código original (para comparação)

### Documentação
- **`relatorio_teorico.md`**: Relatório teórico detalhado da implementação
- **`README_trabalho1.md`**: Este arquivo de documentação

### Imagens Geradas
- **`curved_surfaces_vista_frontal.png`**: Vista frontal (30°, 45°)
- **`curved_surfaces_vista_lateral_direita.png`**: Vista lateral direita (30°, 135°)
- **`curved_surfaces_vista_traseira.png`**: Vista traseira (30°, 225°)
- **`curved_surfaces_vista_lateral_esquerda.png`**: Vista lateral esquerda (30°, 315°)
- **`curved_surfaces_vista_superior.png`**: Vista superior (60°, 45°)
- **`curved_surfaces_vista_inferior.png`**: Vista inferior (0°, 45°)
- **`curved_surfaces_vista_diagonal.png`**: Vista diagonal (45°, 90°)

## Implementações Realizadas

### 1. Superfícies Curvas (Seção 3.2.11)

**Transformação das asas da borboleta:**
- Asas superiores: Esferas com raio 0.6, 256 vértices, 225 faces
- Asas inferiores: Esferas com raio 0.5, 169 vértices, 144 faces
- Uso de coordenadas esféricas para geração de vértices
- Conversão para coordenadas cartesianas: x = r*sin(φ)*cos(θ), y = r*sin(φ)*sin(θ), z = r*cos(φ)

### 2. Sombreamento de Phong (Seção 5.4.4.3)

**Modelo de iluminação completo:**
- Componente ambiente: Ia = 0.3
- Componente difusa: Id = 0.7 * cos(θ)
- Componente especular: Is = 0.8 * (cos(α))^32
- Cálculo do vetor de reflexão: R = 2(N·L)N - L

### 3. Luz Amarelada (Tabela 5.1)

**Implementação de luz colorida:**
- RGB = (1.0, 0.9, 0.7) - Luz amarelada
- Aplicação nas superfícies especulares
- Mantém superfícies difusas com iluminação original

### 4. Diferenciação de Materiais

**Superfícies difusas (fosco):**
- Corpo, cabeça e antenas da borboleta
- Toro base
- Apenas componentes ambiente e difusa

**Superfícies especulares (polido):**
- Asas da borboleta (esferas)
- Componentes ambiente, difusa e especular
- Expoente de brilho n = 32

## Como Executar

### Requisitos
```bash
pip install numpy matplotlib
```

### Execução Interativa
```bash
python comp_graf_curved_surfaces.py
```
- Abre uma janela 3D interativa
- Arraste o mouse para rotacionar a cena
- Visualize as diferenças entre superfícies difusas e especulares

### Geração de Imagens
```bash
python generate_images.py
```
- Gera 7 imagens em diferentes ângulos
- Salva automaticamente no diretório atual

## Estatísticas dos Objetos

### Toro (Base)
- **Vértices**: 400
- **Faces**: 400
- **Material**: Difuso
- **Cor**: Azul (hue = 240)

### Borboleta
- **Total de vértices**: 882
- **Total de faces**: 762
- **Partes difusas**: 32 vértices, 24 faces
- **Partes especulares**: 850 vértices, 738 faces

### Partes da Borboleta
1. **Corpo**: 8 vértices, 6 faces - Difuso
2. **Cabeça**: 8 vértices, 6 faces - Difuso
3. **Antena Esquerda**: 8 vértices, 6 faces - Difuso
4. **Antena Direita**: 8 vértices, 6 faces - Difuso
5. **Asa Superior Esquerda**: 256 vértices, 225 faces - Especular
6. **Asa Superior Direita**: 256 vértices, 225 faces - Especular
7. **Asa Inferior Esquerda**: 169 vértices, 144 faces - Especular
8. **Asa Inferior Direita**: 169 vértices, 144 faces - Especular

## Parâmetros de Iluminação

- **Luz ambiente**: 0.3
- **Luz difusa**: 0.7
- **Luz especular**: 0.8
- **Expoente de brilho**: 32
- **Luz amarelada**: RGB(1.0, 0.9, 0.7)
- **Direção da luz**: (0, 0, 1) - vindo de frente

## Conceitos Teóricos Aplicados

1. **Modelagem de superfícies paramétricas** (Seção 3.2.11)
2. **Coordenadas esféricas e cartesianas**
3. **Modelo de iluminação de Phong** (Seção 5.4.4.3)
4. **Reflexão especular e difusa**
5. **Luz colorida** (Tabela 5.1)
6. **Algoritmo do pintor** para oclusão (Seção 5.3.3.1)
7. **Controles de câmera interativos**

## Resultados Visuais

### Diferenças Observáveis
- **Superfícies planas** (corpo, antenas): Aparência fosca/mate
- **Superfícies curvas** (asas): Aparência brilhante/reflexiva
- **Luz amarelada**: Tonalidade quente nas superfícies especulares
- **Reflexão especular**: Pontos de luz brilhantes nas asas

### Imagens Geradas
As 7 imagens mostram a cena em diferentes ângulos, permitindo visualizar:
- A diferença entre materiais difusos e especulares
- O efeito da luz amarelada
- A forma das superfícies curvas
- A oclusão correta entre objetos

## Sugestões para Compartilhamento

Para que todos da turma possam ver os resultados:

1. **Compartilhar o código**: Todos os arquivos Python
2. **Incluir imagens**: As 7 imagens geradas
3. **Documentação**: Relatório teórico e este README
4. **Demonstração**: Execução interativa em sala
5. **Apresentação**: Slides com comparações antes/depois

## Melhorias Implementadas

### Comparação com o Código Original
- **Antes**: Asas planas (cubos) com iluminação difusa simples
- **Depois**: Asas curvas (esferas) com sombreamento de Phong completo

### Funcionalidades Adicionadas
- Modelagem de superfícies curvas
- Sombreamento de Phong com reflexão especular
- Luz colorida (amarelada)
- Diferenciação de materiais
- Geração automática de imagens
- Documentação teórica completa

## Conclusão

O trabalho demonstra com sucesso a implementação de superfícies curvas e sombreamento de Phong, criando uma cena 3D visualmente rica que diferencia claramente entre superfícies difusas e especulares, iluminadas por luz amarelada conforme especificado. A implementação segue rigorosamente os conceitos teóricos das seções 3.2.11 e 5.4.4.3 do livro texto. 