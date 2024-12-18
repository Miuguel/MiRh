import numpy as np
import numpy as np
from scipy.sparse import diags


def solve_tridiagonal(a, b, c, d):
    """
    Resolve um sistema linear tridiagonal Ax = d usando o Algoritmo de Thomas.
    
    Parâmetros:
    a (array): Subdiagonal (a_1 até a_{n-1})
    b (array): Diagonal principal (b_0 até b_{n-1})
    c (array): Supradiagonal (c_0 até c_{n-2})
    d (array): Vetor do lado direito (d_0 até d_{n-1})

    Retorna:
    x (array): Solução do sistema Ax = d
    """
    n = len(d)
    
    # Modificar os coeficientes
    c_prime = np.zeros(n - 1)
    d_prime = np.zeros(n)

    # Etapa de Eliminação Progressiva
    c_prime[0] = c[0] / b[0]
    d_prime[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] - a[i - 1] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = c[i] / denom
        d_prime[i] = (d[i] - a[i - 1] * d_prime[i - 1]) / denom

    # Etapa de Substituição Retroativa
    x = np.zeros(n)
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]

    return x

# Parâmetros
n = 100  # Número de pontos espaciais
a = -np.ones(n - 1)  # Subdiagonal
b = 2 * np.ones(n)   # Diagonal principal
c = -np.ones(n - 1)  # Supradiagonal
d = np.sin(np.linspace(0, np.pi, n))  # Exemplo de vetor d (condições iniciais)

# Resolver o sistema
x = solve_tridiagonal(a, b, c, d)
print(x)


# Criando uma matriz tridiagonal esparsa
n = 500  # Tamanho da matriz
diagonal = 2 * np.ones(n)       # Diagonal principal
sub_diagonal = -np.ones(n - 1)  # Subdiagonal
super_diagonal = -np.ones(n - 1)  # Supradiagonal

# Criando a matriz esparsa
A = diags([sub_diagonal, diagonal, super_diagonal], offsets=[-1, 0, 1], format="csr")
print(A)  # Isso imprime uma matriz esparsa
