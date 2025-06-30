# Computer Vision - Questionários

Este diretório contém a implementação de questionários sobre técnicas fundamentais de Visão Computacional.

## Estrutura dos Questionários

### ✅ Questionário 2 - Processamento de Cores
**Arquivos**: `Questionario_2/`
- **Parte 1**: Balanço de Branco (White Balance)
  - Correção em espaços RGB e XYZ
  - Iluminantes padrão (D50, D55, D65, D75)
  - `white_balance_correction.py`
- **Parte 2**: Quantização de Cores
  - Quantização uniforme (128, 64, 32 níveis)
  - Quantização não-uniforme (K-means, Median Cut)
  - `color_quantization.py`

### ✅ Questionário 3 - Processamento de Imagens
**Arquivos**: `Questionario_3/`
- **Parte 1**: Equalização de Histograma
  - Implementação manual da equalização
  - Aplicação em imagens com baixo contraste
- **Parte 2**: Filtro da Mediana
  - Redução de ruído sal e pimenta
  - Kernels 3x3, 5x5, 7x7
- **Parte 3**: Remoção de Ruído Espectral
  - Transformada Discreta de Fourier
  - Filtro passa-baixa no domínio da frequência
- `image_processing.py`

### ✅ Questionário 4 - Extração de Features
**Arquivos**: `Questionario_4/`
- **Parte 1**: Features SIFT
  - Detecção de keypoints e descritores
  - Matching com BF e FLANN matchers
- **Parte 2**: Features VGG-16
  - Extração de features de camadas intermediárias
  - Análise de correlação entre features
- **Parte 3**: Análise Comparativa
  - Comparação entre SIFT e VGG-16
  - Avaliação de qualidade para registro de imagens
- `feature_extraction.py`

### ✅ Questionário 5 - Visão Estéreo
**Arquivos**: `Questionario_5/`
- **Parte 1**: Mapa de Disparidade
  - Implementação de janelas de correspondência
  - Tamanhos 1x1, 3x3, 5x5, 7x7
- **Parte 2**: Funções de Custo
  - SSD (Sum of Squared Differences)
  - Correlação normalizada
- **Parte 3**: Análise de Performance
  - Comparação de tempo de processamento
  - Avaliação de qualidade visual
- `stereo_disparity.py`

## Instalação e Execução

### Dependências
```bash
pip install -r requirements.txt
```

### Execução dos Questionários

#### Questionário 2
```bash
cd Questionario_2
python white_balance_correction.py
python color_quantization.py
```

#### Questionário 3
```bash
cd Questionario_3
python image_processing.py
```

#### Questionário 4
```bash
cd Questionario_4
python feature_extraction.py
```

#### Questionário 5
```bash
cd Questionario_5
python stereo_disparity.py
```

## Justificativas Técnicas

### Balanço de Branco (Q2)
- **Espaço RGB**: Simples e rápido, mas pode não ser fisiologicamente correto
- **Espaço XYZ**: Baseado na percepção humana, mais preciso para correção
- **Iluminantes**: D65 é o padrão mais usado, outros ajustam temperatura de cor

### Quantização de Cores (Q2)
- **Uniforme**: Divide espaço igualmente, pode perder detalhes importantes
- **K-means**: Agrupa cores similares, preserva cores mais frequentes
- **Median Cut**: Algoritmo hierárquico, boa qualidade e velocidade

### Equalização de Histograma (Q3)
- **Funcionamento**: Redistribui níveis de intensidade para ocupar toda a faixa
- **Vantagens**: Melhora contraste global, revela detalhes ocultos
- **Limitações**: Pode amplificar ruído, não considera contexto local

### Filtro da Mediana (Q3)
- **Funcionamento**: Substitui pixel pela mediana dos vizinhos
- **Vantagens**: Eficaz contra ruído impulsivo, preserva bordas
- **Tamanhos**: Maior kernel = mais suavização, mas pode perder detalhes

### Remoção de Ruído Espectral (Q3)
- **Funcionamento**: Ruído periódico aparece como picos no domínio da frequência
- **Vantagens**: Remove ruído específico sem afetar outros detalhes
- **Parâmetros**: Raio do filtro determina nível de suavização

### Features SIFT (Q4)
- **Funcionamento**: Features locais invariantes a escala e rotação
- **Vantagens**: Preciso para registro de imagens similares
- **Aplicações**: Matching de pontos correspondentes

### Features VGG-16 (Q4)
- **Funcionamento**: Features semânticas de camadas convolucionais
- **Vantagens**: Captura padrões de alto nível, robusto a variações
- **Camadas**: block1_pool (baixo nível), block3_pool (médio), block5_pool (alto)

### Mapa de Disparidade (Q5)
- **Funcionamento**: Busca correspondência entre imagens estéreo
- **Janelas**: Maior janela = menos ruído, mais lento
- **Funções**: SSD (rápida), Correlação (robusta a iluminação)

## Análise Comparativa

### White Balance
- Correção XYZ produz resultados mais naturais
- Correção RGB é mais rápida mas pode introduzir artefatos
- D65 é o iluminante padrão mais usado

### Quantização
- Uniforme: Rápida mas pode causar posterização
- K-means: Melhor qualidade visual, mais lento
- Median Cut: Boa qualidade, velocidade intermediária

### Filtros
- Mediana 3x3: Remove ruído leve, preserva detalhes
- Mediana 5x5: Bom equilíbrio entre remoção e preservação
- Mediana 7x7: Remove mais ruído, mas pode suavizar demais

### Features
- SIFT: Melhor para imagens similares, registro preciso
- VGG-16: Melhor para correspondência semântica, robusto a variações
- BF Matcher: Mais preciso, FLANN: Mais rápido

### Visão Estéreo
- Janela 1x1: Muito ruidosa, rápida
- Janela 5x5: Bom equilíbrio qualidade/velocidade
- Janela 7x7: Melhor qualidade, mais lenta
- SSD: Mais rápida, Correlação: Mais robusta

## Estrutura de Arquivos

```
Computer Vision/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências unificadas
├── Questionario_2/              # ✅ Completo
│   ├── white_balance_correction.py
│   └── color_quantization.py
├── Questionario_3/              # ✅ Completo
│   └── image_processing.py
├── Questionario_4/              # ✅ Completo
│   └── feature_extraction.py
└── Questionario_5/              # ✅ Completo
    └── stereo_disparity.py
```

## Resultados Esperados

### Questionário 2
- Imagens com correção de white balance (RGB e XYZ)
- Imagens quantizadas (uniforme e não-uniforme)
- Análise comparativa dos métodos

### Questionário 3
- Imagens equalizadas
- Imagens filtradas com diferentes kernels
- Imagem com ruído espectral removido

### Questionário 4
- Matches SIFT entre pares de imagens
- Análise de correlação VGG-16
- Comparação de qualidade de features

### Questionário 5
- Mapas de disparidade para diferentes configurações
- Análise de tempo de processamento
- Comparação visual de resultados

## Melhorias Futuras

- Interface gráfica para ajuste de parâmetros
- Análise quantitativa mais detalhada
- Otimização de performance para imagens grandes
- Implementação de algoritmos mais avançados (SGM, Census)
- Avaliação com ground truth quando disponível 