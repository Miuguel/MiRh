# MiRh: Algoritmos de Deconvolução e Simulação de Calor

## Descrição
Este projeto implementa algoritmos de simulação de calor (ADI) e deconvolução cega de imagens (BID), baseados em artigos científicos, incluindo o uso da matriz resultante de Sylvester. O objetivo é estudar e demonstrar técnicas de processamento de imagens e restauração.

- Borramento de imagens usando o método ADI (Alternating Direction Implicit)
- Deconvolução cega (Blind Image Deconvolution, BID) baseada em Sylvester
- Exemplos com imagens clássicas (ex: cameraman)

---

## Instalação

1. Clone o repositório:
   ```bash
   git clone <repo-url>
   cd MiRh
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou 'Scripts/activate' no Windows
   pip install -r requirements.txt
   ```

---

## Estrutura do Projeto

- `src/` — Código principal
- `old/` — Códigos antigos ou de referência
- `examples/` — Imagens de entrada e saída
- `requirements.txt` — Dependências

---

## Algoritmos
- **ADI:** Simulação de calor para borramento de imagens
- **BID:** Deconvolução cega baseada em matriz de Sylvester

Referências principais:
- Winkler, The Sylvester resultant matrix and image

---

## Licença
Veja o arquivo LICENSE. 