# MiRh

**MiRh** é um projeto experimental que explora a aplicação de métodos numéricos para cálculos em diversas simulações. A ideia principal é utilizar conceitos de cálculo, como equações diferenciais e métodos de aproximação, para criar representações visuais interativas, como simulações de fenômenos físicos (ex.: propagação de calor) aplicadas em imagens com o uso de cores.

## 🧮 Objetivo

O objetivo do **MiRh** é demonstrar o poder e a versatilidade de métodos numéricos em resolver problemas complexos, enquanto transforma os resultados em representações visuais que facilitam a interpretação. A principal aplicação explorada até agora envolve a propagação de calor simulada em imagens, representada por alterações de cores.

## 🚀 Funcionalidades

- Simulações baseadas em métodos numéricos, como diferenças finitas.
- Representação gráfica da propagação de valores (como calor) sobre uma matriz de pixels.
- Conversão dos resultados dos cálculos em transformações visuais, usando cores para representar diferentes estados.

## 📂 Estrutura do Projeto

```plaintext
MiRh/
├── src/
│   ├── heat_spread_simulation.py  # Simulação de propagação de calor em imagens
│   ├── numerical_methods.py       # Métodos numéricos implementados
│   └── utils.py                   # Funções auxiliares
├── examples/
│   ├── example_image.jpg          # Exemplo de imagem para simulação
│   └── heat_simulation_output.png # Resultado da simulação
├── README.md                      # Documentação do projeto
├── requirements.txt               # Dependências do projeto
└── LICENSE                        # Licença do projeto
```

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal para cálculos e simulações.
- **NumPy**: Para operações matriciais eficientes.
- **Matplotlib**: Para plotagem e visualização de resultados.
- **Pillow (PIL)**: Para manipulação de imagens.

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/MiRh.git
   cd MiRh
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Como Usar

1. Certifique-se de que você possui uma imagem no formato `.jpg` ou `.png` para a simulação.
2. Execute o script principal:
   ```bash
   python src/heat_spread_simulation.py --image examples/example_image.jpg
   ```
3. O resultado será salvo como um arquivo na pasta `examples/`, mostrando como o "calor" se espalha pela imagem.

## 🌟 Exemplos

### Imagem Original:
![Imagem Original](examples/example_image.jpg)

### Resultado:
![Resultado](examples/heat_simulation_output.png)

## 🧠 Próximos Passos

- Implementar novos métodos numéricos para outras simulações.
- Adicionar suporte para mais tipos de fenômenos (ex.: propagação de ondas).
- Melhorar a interface visual do programa.
- Criar um painel interativo para ajustar parâmetros da simulação.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Para maiores informações, veja o arquivo `CONTRIBUTING.md`.

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
