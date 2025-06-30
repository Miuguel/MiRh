import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import os

class FeatureExtractor:
    def __init__(self):
        # Inicializa SIFT
        self.sift = cv2.SIFT_create()
        
        # Inicializa VGG-16
        self.vgg_model = VGG16(weights='imagenet', include_top=False)
        
        # Seleciona camadas específicas para extração de features
        # Camadas intermediárias que capturam features de diferentes níveis
        self.vgg_layers = {
            'block1_pool': self.vgg_model.get_layer('block1_pool').output,  # Features de baixo nível
            'block3_pool': self.vgg_model.get_layer('block3_pool').output,  # Features de médio nível
            'block5_pool': self.vgg_model.get_layer('block5_pool').output   # Features de alto nível
        }
        
        # Cria modelos para cada camada
        self.vgg_extractors = {}
        for layer_name, layer_output in self.vgg_layers.items():
            self.vgg_extractors[layer_name] = Model(inputs=self.vgg_model.input, outputs=layer_output)
    
    def extract_sift_features(self, img):
        """Extrai features SIFT da imagem"""
        # Converte para escala de cinza se necessário
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Detecta keypoints e computa descritores
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def extract_vgg_features(self, img, layer_name='block3_pool'):
        """Extrai features VGG-16 de uma camada específica"""
        # Redimensiona imagem para entrada da VGG-16 (224x224)
        img_resized = cv2.resize(img, (224, 224))
        
        # Converte BGR para RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Preprocessa para VGG-16
        img_array = image.img_to_array(img_rgb)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Extrai features
        features = self.vgg_extractors[layer_name].predict(img_array)
        
        return features
    
    def match_features(self, desc1, desc2, method='bf'):
        """Realiza matching de features"""
        if method == 'bf':
            # Brute Force Matcher
            matcher = cv2.BFMatcher()
        else:
            # FLANN Matcher (mais rápido para grandes conjuntos)
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            matcher = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Realiza matching
        matches = matcher.knnMatch(desc1, desc2, k=2)
        
        # Aplica filtro de Lowe's ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def draw_matches(self, img1, img2, kp1, kp2, matches, title, filename):
        """Desenha matches entre duas imagens"""
        # Desenha matches
        img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        
        # Salva resultado
        cv2.imwrite(filename, img_matches)
        
        # Plota resultado
        plt.figure(figsize=(20, 10))
        plt.imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"plot_{filename}", dpi=300, bbox_inches='tight')
        plt.close()
        
        return len(matches)

def analyze_feature_quality(img1, img2, extractor, pair_name):
    """Analisa qualidade das features para um par de imagens"""
    print(f"\n=== ANÁLISE: {pair_name} ===")
    
    # Extrai features SIFT
    print("Extraindo features SIFT...")
    kp1_sift, desc1_sift = extractor.extract_sift_features(img1)
    kp2_sift, desc2_sift = extractor.extract_sift_features(img2)
    
    print(f"SIFT - Imagem 1: {len(kp1_sift)} keypoints")
    print(f"SIFT - Imagem 2: {len(kp2_sift)} keypoints")
    
    # Extrai features VGG-16 de diferentes camadas
    print("Extraindo features VGG-16...")
    vgg_features = {}
    for layer_name in ['block1_pool', 'block3_pool', 'block5_pool']:
        feat1 = extractor.extract_vgg_features(img1, layer_name)
        feat2 = extractor.extract_vgg_features(img2, layer_name)
        vgg_features[layer_name] = (feat1, feat2)
        print(f"VGG-16 {layer_name}: {feat1.shape} -> {feat2.shape}")
    
    # Matching SIFT
    if desc1_sift is not None and desc2_sift is not None:
        print("\nRealizando matching SIFT...")
        sift_matches_bf = extractor.match_features(desc1_sift, desc2_sift, 'bf')
        sift_matches_flann = extractor.match_features(desc1_sift, desc2_sift, 'flann')
        
        print(f"SIFT BF Matcher: {len(sift_matches_bf)} matches")
        print(f"SIFT FLANN Matcher: {len(sift_matches_flann)} matches")
        
        # Desenha matches SIFT
        if len(sift_matches_bf) > 0:
            extractor.draw_matches(img1, img2, kp1_sift, kp2_sift, sift_matches_bf,
                                 f"SIFT Matches - {pair_name} (BF)",
                                 f"sift_matches_bf_{pair_name}.png")
        
        if len(sift_matches_flann) > 0:
            extractor.draw_matches(img1, img2, kp1_sift, kp2_sift, sift_matches_flann,
                                 f"SIFT Matches - {pair_name} (FLANN)",
                                 f"sift_matches_flann_{pair_name}.png")
    
    # Matching VGG-16 (usando correção entre features)
    print("\nAnalisando features VGG-16...")
    for layer_name, (feat1, feat2) in vgg_features.items():
        # Calcula correlação entre features
        feat1_flat = feat1.flatten()
        feat2_flat = feat2.flatten()
        
        # Garante que têm o mesmo tamanho
        min_size = min(len(feat1_flat), len(feat2_flat))
        feat1_flat = feat1_flat[:min_size]
        feat2_flat = feat2_flat[:min_size]
        
        correlation = np.corrcoef(feat1_flat, feat2_flat)[0, 1]
        print(f"VGG-16 {layer_name} correlação: {correlation:.4f}")
    
    return {
        'sift_keypoints': (len(kp1_sift), len(kp2_sift)),
        'sift_matches_bf': len(sift_matches_bf) if desc1_sift is not None and desc2_sift is not None else 0,
        'sift_matches_flann': len(sift_matches_flann) if desc1_sift is not None and desc2_sift is not None else 0,
        'vgg_correlations': {layer: np.corrcoef(feat1.flatten()[:1000], feat2.flatten()[:1000])[0, 1] 
                           for layer, (feat1, feat2) in vgg_features.items()}
    }

def main():
    print("=== QUESTIONÁRIO 4 - EXTRAÇÃO DE FEATURES ===\n")
    
    # Inicializa extrator de features
    extractor = FeatureExtractor()
    
    # Lista de pares de imagens para análise
    image_pairs = [
        ("Bricks1", "Questionario-4-Bricks1.jpg", "Questionario-4-Bricks2.jpg"),
        ("Building1", "Questionario-4-Building1.jpg", "Questionario-4-Building2.jpg"),
        ("Cats", "Questionario-4-Gatos1.jpg", "Questionario-4-Paisagem1.jpg")  # Par próprio
    ]
    
    results = {}
    
    # Analisa cada par de imagens
    for pair_name, img1_path, img2_path in image_pairs:
        print(f"\nProcessando par: {pair_name}")
        
        # Carrega imagens
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        
        if img1 is None or img2 is None:
            print(f"Erro: Não foi possível carregar {img1_path} ou {img2_path}")
            continue
        
        print(f"Imagem 1: {img1.shape}")
        print(f"Imagem 2: {img2.shape}")
        
        # Analisa qualidade das features
        result = analyze_feature_quality(img1, img2, extractor, pair_name)
        results[pair_name] = result
    
    # Relatório final
    print("\n" + "="*60)
    print("RELATÓRIO FINAL - ANÁLISE DE FEATURES")
    print("="*60)
    
    for pair_name, result in results.items():
        print(f"\n{pair_name}:")
        print(f"  SIFT Keypoints: {result['sift_keypoints'][0]} -> {result['sift_keypoints'][1]}")
        print(f"  SIFT Matches (BF): {result['sift_matches_bf']}")
        print(f"  SIFT Matches (FLANN): {result['sift_matches_flann']}")
        print(f"  VGG-16 Correlações:")
        for layer, corr in result['vgg_correlations'].items():
            print(f"    {layer}: {corr:.4f}")
    
    # Análise comparativa
    print("\n" + "="*60)
    print("ANÁLISE COMPARATIVA")
    print("="*60)
    
    print("\nSIFT vs VGG-16 Features:")
    print("- SIFT: Features locais, invariantes a escala e rotação")
    print("- VGG-16: Features semânticas, capturam padrões de alto nível")
    print("- SIFT é melhor para registro preciso de imagens similares")
    print("- VGG-16 é melhor para correspondência semântica")
    
    print("\nMatching Methods:")
    print("- BF Matcher: Mais preciso, mas mais lento")
    print("- FLANN Matcher: Mais rápido, boa precisão para grandes conjuntos")
    
    print("\nQualidade por Tipo de Imagem:")
    print("- Imagens similares (Bricks, Buildings): SIFT funciona bem")
    print("- Imagens diferentes (Cats vs Landscape): VGG-16 pode ser melhor")
    
    print("\nArquivos gerados:")
    for pair_name, _, _ in image_pairs:
        print(f"- sift_matches_bf_{pair_name}.png")
        print(f"- sift_matches_flann_{pair_name}.png")
        print(f"- plot_sift_matches_bf_{pair_name}.png")
        print(f"- plot_sift_matches_flann_{pair_name}.png")

if __name__ == "__main__":
    main() 