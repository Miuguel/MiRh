# Experimentos de Computação Gráfica

Este diretório contém dois experimentos práticos de Computação Gráfica implementados em Python.

## 📋 Experimentos Disponíveis

### 1. **Balanço do Branco (White Balance)**
- **Arquivo**: `white_balance_experiment.py`
- **Objetivo**: Ajustar o balanço do branco de uma imagem
- **Espaços de cor**: RGB e XYZ
- **Iluminantes**: D50, D55, D65, D75

### 2. **Quantização de Cores**
- **Arquivo**: `color_quantization_experiment.py`
- **Objetivo**: Reduzir o número de cores em uma imagem
- **Métodos**: Quantização uniforme e K-means
- **Níveis**: 128, 64 e 32 cores

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install -r requirements_experiments.txt
```

### Execução Automática
```bash
python run_experiments.py
```

### Execução Individual
```bash
# Balanço do branco
python white_balance_experiment.py

# Quantização de cores
python color_quantization_experiment.py
```

## 📸 Como Usar com Suas Próprias Imagens

### Para o Experimento de Balanço do Branco:

1. **Fotografe uma cena** com uma folha branca de papel e objetos coloridos
2. **Desligue o balanço automático** da sua câmera
3. **Edite o código** em `white_balance_experiment.py`:

```python
# Substitua esta linha:
experiment = WhiteBalanceExperiment("sample_image.jpg")

# Por:
experiment = WhiteBalanceExperiment("sua_imagem.jpg")

# Ajuste as coordenadas da região branca:
experiment.select_white_region(x1, y1, x2, y2)  # Coordenadas do papel branco
```

### Para o Experimento de Quantização:

1. **Fotografe uma parte da sua casa** com resolução máxima
2. **Edite o código** em `color_quantization_experiment.py`:

```python
# Substitua esta linha:
experiment = ColorQuantizationExperiment("sample_image.jpg")

# Por:
experiment = ColorQuantizationExperiment("sua_imagem.jpg")
```

## 📁 Estrutura de Arquivos

```
src/examples/
├── white_balance_experiment.py      # Experimento 1
├── color_quantization_experiment.py # Experimento 2
├── run_experiments.py              # Script principal
├── requirements_experiments.txt     # Dependências
├── README_experimentos.md          # Este arquivo
├── white_balance_results/          # Resultados do exp. 1
└── quantization_results/           # Resultados do exp. 2
```

## 📊 Resultados Gerados

### Balanço do Branco:
- `original.png` - Imagem original
- `rgb_D50.png`, `rgb_D55.png`, `rgb_D65.png`, `rgb_D75.png` - Resultados RGB
- `xyz_D50.png`, `xyz_D55.png`, `xyz_D65.png`, `xyz_D75.png` - Resultados XYZ

### Quantização de Cores:
- `original.png` - Imagem original
- `uniform_128.png`, `uniform_64.png`, `uniform_32.png` - Quantização uniforme
- `kmeans_128.png`, `kmeans_64.png`, `kmeans_32.png` - Quantização K-means
- `palette_128.png`, `palette_64.png`, `palette_32.png` - Paletas de cores

## 🔧 Personalização

### Ajustar Coordenadas da Região Branca:
```python
# Para uma imagem 1920x1080, se o papel branco está no centro:
experiment.select_white_region(800, 400, 1120, 680)
```

### Modificar Níveis de Quantização:
```python
# No arquivo color_quantization_experiment.py:
self.quantization_levels = [256, 128, 64, 32, 16]  # Mais níveis
```

### Adicionar Novos Iluminantes:
```python
# No arquivo white_balance_experiment.py:
self.illuminants['D40'] = [0.9800, 1.0000, 0.7500]
```

## 📈 Análise dos Resultados

### Balanço do Branco:
- **RGB**: Correção direta nos canais vermelho, verde e azul
- **XYZ**: Correção no espaço de cores perceptualmente uniforme
- **Comparação**: Observe as diferenças entre os métodos

### Quantização:
- **Uniforme**: Distribuição igual dos níveis de cor
- **K-means**: Distribuição adaptativa baseada no conteúdo
- **Qualidade**: K-means geralmente produz resultados mais naturais

## 🐛 Solução de Problemas

### Erro: "Não foi possível carregar a imagem"
- Verifique se o caminho da imagem está correto
- Certifique-se de que a imagem existe no local especificado

### Erro: "Região branca não foi selecionada"
- Ajuste as coordenadas da região branca no código
- Use ferramentas de visualização para encontrar as coordenadas corretas

### Erro de dependências:
```bash
pip install --upgrade pip
pip install -r requirements_experiments.txt
```

## 📝 Relatório

Para incluir no seu relatório:

1. **Imagens originais** capturadas por você
2. **Códigos fonte** dos experimentos
3. **Imagens processadas** geradas pelos programas
4. **Análise comparativa** dos resultados
5. **Conclusões** sobre os métodos utilizados

## 🎯 Objetivos de Aprendizado

- Compreender o conceito de balanço do branco
- Entender diferentes espaços de cores (RGB vs XYZ)
- Aprender métodos de quantização de cores
- Comparar quantização uniforme vs adaptativa
- Analisar qualidade visual dos resultados 