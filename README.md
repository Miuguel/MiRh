# MiRh

**MiRh** é um projeto experimental que explora a aplicação de métodos numéricos para cálculos em simulações de equações diferenciais parabólicas relacionadas à distribuição de calor em uma chapa 2D. A ideia principal é utilizar conceitos de cálculo, como equações diferenciais e métodos de aproximação, para criar representações visuais interativas, simulando fenômenos físicos por meio de cores.

📄 *For the English version of this README, click here: [README.en.md](README.en.md)*

## 🧮 Objetivo

O objetivo do **MiRh** é o aprendizado de diversos conceitos de cálculo e programação, demonstrando a versatilidade dos métodos numéricos na resolução de problemas complexos. A principal aplicação explorada até agora envolve a propagação de calor simulada em imagens, representada por alterações de cores.

## 🚀 Funcionalidades

- Simulações baseadas em métodos numéricos.
- Representação gráfica da propagação de valores (como calor) sobre uma matriz de pixels.
- Conversão dos resultados dos cálculos em transformações visuais, usando cores para representar diferentes estados.

## 📂 Estrutura do Projeto

```plaintext
MiRh/
├── src/         
│   ├── adi_simulation.py          # Alternating Directions Implicit - Método implícito mais otimizado até agora
│   ├── conv_FFT_simulation.py     # Otimização da convolução usando Fast Fourier Transform
│   ├── conv_simulation.py         # Resolução da EDO usando convolução e kernel
│   ├── heat_simulation.py         # Versão em Python da simulação otimizada do MATLAB
│   ├── heat_spread_sim_otim.m     # Otimização usando operações matriciais em vez de loops
│   ├── heat_spread_sim.m          # Simulação de propagação de calor em matriz com MATLAB
│   ├── main.py                    # Arquivo principal
│   ├── metodo_implicito.py        # Métodos implícitos retirados do livro da Valeria
│   └── utils.py                   # Funções auxiliares
├── examples/
│   ├── example_image.jpg          # Exemplo de imagem para simulação
│   └── heat_simulation_output.jpg # Resultado da simulação
├── README.md                      # Documentação do projeto (PT-BR)
├── README.en.md                   # Documentação do projeto (EN)
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
   git clone https://github.com/Miuguel/MiRh.git
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
![Imagem Original](examples/example_image.png)

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

---

## 📖 Motivação & Evolução do Projeto

Este projeto começou como uma aplicação computacional para resolver a equação de calor em um espaço bidimensional, inicialmente utilizando loops. Depois, como um exercício de otimização, as operações foram substituídas por cálculos matriciais. No entanto, em algumas situações, a solução tornava-se instável.

Foi então que meu orientador, Ralph, explicou que o que eu havia feito era equivalente a aplicar uma **convolução** com um kernel específico sobre a matriz que representava o espaço bidimensional. Ele também me ensinou sobre a **condição de estabilidade de Von Neumann** e sobre o **método de Crank-Nicholson**, desenvolvido por John Crank e Phyllis Nicolson, que resolve essa equação diferencial de forma implícita e estável.

Entretanto, o livro que consultei (*EDP - Um Curso de Graduação*, escrito por Valeria Iório) apresentava o algoritmo em uma dimensão. Para torná-lo bidimensional, haveria um crescimento exponencial no tamanho da matriz a ser resolvida, mesmo utilizando métodos para lidar com matrizes esparsas.

Foi então que tive a ideia de dividir o problema e resolver alternadamente em cada direção. Ao pesquisar mais, descobri o **Método Implícito de Direções Alternadas (ADI)**, que não só é **implícito (portanto, estável)**, mas também permite otimizar a resolução da equação matricial de Sylvester **(AX + XB = C)** utilizando a estrutura esparsa da matriz.
```
