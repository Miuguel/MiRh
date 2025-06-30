#!/usr/bin/env python3
"""
Script principal para executar os experimentos de Computação Gráfica
"""

import os
import sys
import zipfile
from datetime import datetime

def install_requirements():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    os.system("pip install -r requirements_experiments.txt")

def run_white_balance_experiment():
    """Executa o experimento de balanço do branco"""
    print("\n" + "="*50)
    print("EXPERIMENTO 1: BALANÇO DO BRANCO")
    print("="*50)
    
    try:
        from white_balance_experiment import main as wb_main
        wb_main()
        print(" Experimento de balanço do branco concluído!")
        return True
    except Exception as e:
        print(f" Erro no experimento de balanço do branco: {e}")
        return False

def run_quantization_experiment():
    """Executa o experimento de quantização de cores"""
    print("\n" + "="*50)
    print("EXPERIMENTO 2: QUANTIZAÇÃO DE CORES")
    print("="*50)
    
    try:
        from color_quantization_experiment import main as q_main
        q_main()
        print(" Experimento de quantização de cores concluído!")
        return True
    except Exception as e:
        print(f" Erro no experimento de quantização de cores: {e}")
        return False

def create_results_zip():
    """Cria um arquivo ZIP com todos os resultados"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"experimentos_cg_{timestamp}.zip"
    
    print(f"\nCriando arquivo ZIP: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Adiciona códigos fonte
        source_files = [
            'white_balance_experiment.py',
            'color_quantization_experiment.py',
            'run_experiments.py',
            'requirements_experiments.txt'
        ]
        
        for file in source_files:
            if os.path.exists(file):
                zipf.write(file, f"codigo_fonte/{file}")
                print(f"   Adicionado: codigo_fonte/{file}")
        
        # Adiciona resultados do balanço do branco
        if os.path.exists("white_balance_results"):
            for root, dirs, files in os.walk("white_balance_results"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arc_path)
                    print(f"   Adicionado: {arc_path}")
        
        # Adiciona resultados da quantização
        if os.path.exists("quantization_results"):
            for root, dirs, files in os.walk("quantization_results"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arc_path)
                    print(f"   Adicionado: {arc_path}")
    
    print(f"\n📦 Arquivo ZIP criado com sucesso: {zip_filename}")
    return zip_filename

def main():
    """Função principal"""
    print(" EXPERIMENTOS DE COMPUTAÇÃO GRÁFICA")
    print("="*50)
    print("Este script executa dois experimentos:")
    print("1. Balanço do branco (RGB e XYZ)")
    print("2. Quantização de cores (uniforme e K-means)")
    print("\n  IMPORTANTE: Para usar suas próprias imagens:")
    print("   - Substitua 'sample_image.jpg' pelos caminhos das suas imagens")
    print("   - Ajuste as coordenadas das regiões nos códigos")
    print("   - Execute novamente o script")
    
    # Verifica se as dependências estão instaladas
    try:
        import cv2
        import numpy
        import matplotlib
        import sklearn
        import colorspacious
    except ImportError:
        print("\n Instalando dependências...")
        install_requirements()
    
    # Executa os experimentos
    wb_success = run_white_balance_experiment()
    q_success = run_quantization_experiment()
    
    if wb_success and q_success:
        # Cria arquivo ZIP com resultados
        zip_file = create_results_zip()
        
        print("\n" + "="*50)
        print(" TODOS OS EXPERIMENTOS CONCLUÍDOS!")
        print("="*50)
        print(f" Arquivo ZIP com resultados: {zip_file}")
        print("\n Conteúdo do ZIP:")
        print("   - Códigos fonte dos experimentos")
        print("   - Imagens processadas (balanço do branco)")
        print("   - Imagens quantizadas")
        print("   - Paletas de cores geradas")
        print("\n Para usar com suas imagens:")
        print("   1. Abra os arquivos .py")
        print("   2. Substitua 'sample_image.jpg' pelo caminho da sua imagem")
        print("   3. Ajuste as coordenadas das regiões")
        print("   4. Execute novamente")
    else:
        print("\n Alguns experimentos falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main() 