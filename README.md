# MiRh 2.0

**MiRh 2.0** é a nova geração do projeto de simulação numérica de propagação de calor e outros fenômenos em 2D, com código modular, limpo e preparado para expansão.

## ✨ Novidades da Versão 2.0
- Estrutura reorganizada e modular
- Simuladores otimizados em `src/simulation/`
- Código legado e experimentos antigos movidos para a pasta `old/`
- Pronto para novas funcionalidades e contribuições

## 🚀 Estrutura do Projeto
```plaintext
MiRh/
├── src/
│   ├── main.py                # Ponto de entrada principal
│   ├── image_processing.py    # Funções para manipulação de imagens
│   ├── utils.py               # Utilitários gerais
│   └── simulation/            # Simuladores modernos e otimizados
├── examples/                  # Imagens e resultados de exemplo
├── old/                       # Código legado e versões antigas
├── requirements.txt           # Dependências
├── README.md                  # Este arquivo
└── LICENSE
```

## 🛠️ Tecnologias
- Python 3.8+
- NumPy
- Matplotlib
- Pillow

## 📦 Instalação
```bash
git clone https://github.com/seuusuario/MiRh.git
cd MiRh
python -m venv .venv
.venv\Scripts\activate  # No Windows
pip install -r requirements.txt
```

## 📊 Como Usar
Execute o ponto de entrada principal ou scripts em `src/simulation/` para rodar simulações. Exemplo:
```bash
python src/main.py
```
Consulte o código e os exemplos para explorar diferentes simulações e parâmetros.

## 🤝 Contribua!
Pull requests e sugestões são bem-vindos! Veja o código em `src/` e contribua para a evolução do projeto.

## 📜 Licença
MIT License

---

> Para acessar o código legado, documentação antiga e experimentos, veja a pasta `old/`. 