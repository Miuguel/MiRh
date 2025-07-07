#!/usr/bin/env python3
"""
Script para converter o relatório markdown para PDF
Requer: pip install markdown weasyprint
"""

import markdown
import os
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def markdown_to_pdf(markdown_file, pdf_file):
    """Converte um arquivo markdown para PDF"""
    
    # Lê o arquivo markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Converte markdown para HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
    
    # Adiciona estilos CSS para melhor formatação
    css_content = """
    body {
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        margin: 2cm;
        font-size: 12pt;
    }
    h1 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    h2 {
        color: #34495e;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 5px;
    }
    h3 {
        color: #7f8c8d;
    }
    code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    pre {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        overflow-x: auto;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    ul, ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    li {
        margin: 5px 0;
    }
    """
    
    # Cria o HTML completo
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Relatório Teórico: Superfícies Curvas e Sombreamento de Phong</title>
        <style>{css_content}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Configuração de fontes
    font_config = FontConfiguration()
    
    # Cria o PDF
    HTML(string=full_html).write_pdf(pdf_file, font_config=font_config)
    
    print(f"PDF gerado com sucesso: {pdf_file}")

def main():
    """Função principal"""
    print("=== CONVERTENDO RELATÓRIO PARA PDF ===")
    
    # Arquivos de entrada e saída
    markdown_file = "relatorio_teorico.md"
    pdf_file = "relatorio_teorico.pdf"
    
    # Verifica se o arquivo markdown existe
    if not os.path.exists(markdown_file):
        print(f"Erro: Arquivo {markdown_file} não encontrado!")
        return
    
    try:
        # Converte para PDF
        markdown_to_pdf(markdown_file, pdf_file)
        print(f"Relatório convertido com sucesso para: {pdf_file}")
        
    except ImportError as e:
        print("Erro: Dependências não encontradas!")
        print("Instale as dependências com: pip install markdown weasyprint")
        print(f"Erro detalhado: {e}")
        
    except Exception as e:
        print(f"Erro ao converter para PDF: {e}")

if __name__ == "__main__":
    main() 