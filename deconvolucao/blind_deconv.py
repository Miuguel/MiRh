import numpy as np
from scipy.linalg import solve_sylvester, svd
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class DeconvolutionResult:
    """Container for deconvolution results."""
    restored_image: np.ndarray
    estimated_psf: np.ndarray
    psnr: float
    ssim: float
    mse: float

class BlindDeconvolution:
    """
    Deconvolução cega de imagens usando equações de Sylvester,
    conforme o artigo de Winkler (The Sylvester resultant matrix and image).
    """
    
    def __init__(self, max_psf_size: int = 15, regularization: float = 1e-6):
        """
        Inicializa o resolvedor de deconvolução cega.
        max_psf_size: Tamanho máximo do PSF a ser estimado
        regularization: Parâmetro de regularização para estabilidade numérica
        """
        self.max_psf_size = max_psf_size
        self.regularization = regularization
        self._estimated_psf = None
    
    def _build_sylvester_matrix(self, row1: np.ndarray, row2: np.ndarray, degree: int) -> np.ndarray:
        """
        Constrói a matriz de Sylvester para dois vetores (linhas ou colunas da imagem).
        Cada linha representa os coeficientes de um polinômio associado à imagem borrada.
        degree: grau estimado do PSF.
        """
        n = len(row1)
        S = np.zeros((2*n-degree, 2*n-degree))
        # Preenche o bloco superior com row1
        for i in range(n-degree):
            S[i:i+n, i] = row1
        # Preenche o bloco inferior com row2
        for i in range(n-degree):
            S[i:i+n, n-degree+i] = row2
        return S
    
    def _estimate_psf_degree(self, S: np.ndarray) -> int:
        """
        Estima o grau do PSF analisando os valores singulares da matriz de Sylvester.
        O ponto de "joelho" indica o grau mais provável.
        """
        _, s, _ = svd(S)
        s_normalized = s / s[0]
        diff = np.diff(s_normalized)
        knee_point = np.argmax(diff) + 1
        return knee_point
    
    def _estimate_1d_psf(self, image: np.ndarray, axis: int = 0) -> np.ndarray:
        """
        Estima o PSF 1D ao longo de um eixo (linhas ou colunas) usando equações de Sylvester.
        Usa as duas primeiras linhas/colunas da imagem borrada.
        """
        if axis == 0:
            rows = [image[i, :] for i in range(min(2, image.shape[0]))]
        else:
            rows = [image[:, i] for i in range(min(2, image.shape[1]))]
        S = self._build_sylvester_matrix(rows[0], rows[1], self.max_psf_size)
        degree = self._estimate_psf_degree(S)
        # Resolve a equação de Sylvester via SVD
        _, s, vh = svd(S)
        psf = vh[degree-1, :degree]
        return psf / np.sum(psf)  # Normaliza o PSF
    
    def estimate_psf(self, blurred_image: np.ndarray) -> np.ndarray:
        """
        Estima o PSF 2D separável a partir da imagem borrada.
        Aplica o método 1D em ambos os eixos e combina via produto externo.
        """
        psf_x = self._estimate_1d_psf(blurred_image, axis=0)
        psf_y = self._estimate_1d_psf(blurred_image, axis=1)
        psf_2d = np.outer(psf_y, psf_x)
        self._estimated_psf = psf_2d / np.sum(psf_2d)
        return self._estimated_psf
    
    def deconvolve(self, blurred_image: np.ndarray) -> DeconvolutionResult:
        """
        Realiza a deconvolução cega na imagem borrada.
        1. Estima o PSF se necessário.
        2. Monta matrizes Toeplitz para cada dimensão.
        3. Resolve a equação de Sylvester para restaurar a imagem.
        4. Calcula métricas de qualidade.
        """
        if self._estimated_psf is None:
            self.estimate_psf(blurred_image)
        h, w = blurred_image.shape
        psf_h, psf_w = self._estimated_psf.shape
        # Monta matrizes Toeplitz para cada dimensão
        H_x = np.zeros((w, w))
        H_y = np.zeros((h, h))
        for i in range(w):
            H_x[i, max(0, i-psf_w+1):i+1] = self._estimated_psf[0, :min(psf_w, i+1)][::-1]
        for i in range(h):
            H_y[i, max(0, i-psf_h+1):i+1] = self._estimated_psf[:min(psf_h, i+1), 0][::-1]
        # Adiciona regularização para estabilidade
        H_x += self.regularization * np.eye(w)
        H_y += self.regularization * np.eye(h)
        # Resolve a equação de Sylvester: H_y X + X H_x = imagem_borrada
        restored = solve_sylvester(H_y, H_x, blurred_image)
        # Calcula métricas
        mse = np.mean((blurred_image - restored) ** 2)
        psnr = 10 * np.log10(1.0 / mse)
        ssim = self._calculate_ssim(blurred_image, restored)
        return DeconvolutionResult(
            restored_image=restored,
            estimated_psf=self._estimated_psf,
            psnr=psnr,
            ssim=ssim,
            mse=mse
        )
    
    def _calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Calcula o índice de similaridade estrutural (SSIM) entre duas imagens.
        """
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        kernel = np.ones((11, 11)) / 121
        mu1 = np.convolve(img1.flatten(), kernel.flatten(), mode='valid')
        mu2 = np.convolve(img2.flatten(), kernel.flatten(), mode='valid')
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = np.convolve(img1.flatten() ** 2, kernel.flatten(), mode='valid') - mu1_sq
        sigma2_sq = np.convolve(img2.flatten() ** 2, kernel.flatten(), mode='valid') - mu2_sq
        sigma12 = np.convolve(img1.flatten() * img2.flatten(), kernel.flatten(), mode='valid') - mu1_mu2
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        return np.mean(ssim_map) 