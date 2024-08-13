import numpy as np
import time
import matplotlib.pyplot as plt

def funcao_calor_matrix(matrix, num_iterations, variacao):
    """
    Função para atualizar a matriz
    matrix: matriz inicial (numpy array)
    num_iterations: número de iterações
    variacao: delta x (pequeno fator de variação)
    """
    rows, cols = matrix.shape  # Tamanho da matriz

    for _ in range(num_iterations):
        new_matrix = matrix.copy()  # Cópia da matriz original para atualizar valores

        for i in range(rows):
            for j in range(cols):
                # Calcular a soma dos vizinhos adjacentes
                sum_neighbors = 0
                num_neighbors = 0

                if i > 0:
                    sum_neighbors += matrix[i-1, j]  # Célula acima
                    num_neighbors += 1

                if i < rows - 1:
                    sum_neighbors += matrix[i+1, j]  # Célula abaixo
                    num_neighbors += 1

                if j > 0:
                    sum_neighbors += matrix[i, j-1]  # Célula à esquerda
                    num_neighbors += 1

                if j < cols - 1:
                    sum_neighbors += matrix[i, j+1]  # Célula à direita
                    num_neighbors += 1

                # Atualizar a célula atual baseada na média dos vizinhos
                if num_neighbors > 0:
                    new_matrix[i, j] = matrix[i, j] + variacao * (sum_neighbors / num_neighbors - matrix[i, j])

        matrix = new_matrix  # Atualizar a matriz original com a nova matriz

    return matrix  # Retornar a matriz atualizada

def funcao_calor_otim_matrix(matrix, num_iterations, variacao):
    # Função para atualizar a matriz
    rows, cols = matrix.shape  # Tamanho da matriz

    for _ in range(num_iterations):
        # Criar matrizes deslocadas
        matrix_up = np.vstack([matrix[1:, :], np.zeros((1, cols))])
        matrix_down = np.vstack([np.zeros((1, cols)), matrix[:-1, :]])
        matrix_left = np.hstack([matrix[:, 1:], np.zeros((rows, 1))])
        matrix_right = np.hstack([np.zeros((rows, 1)), matrix[:, :-1]])

        # Soma das matrizes deslocadas
        sum_neighbors = matrix_up + matrix_down + matrix_left + matrix_right

        # Número de vizinhos válidos
        num_neighbors = (matrix_up != 0) + (matrix_down != 0) + (matrix_left != 0) + (matrix_right != 0)

        # Evitar divisão por zero
        num_neighbors[num_neighbors == 0] = 1

        # Calcular a nova matriz com a fórmula fornecida
        new_matrix = matrix + variacao * (sum_neighbors / num_neighbors - matrix)

        # Atualizar a matriz original com a nova matriz
        matrix = new_matrix

    return matrix  # Retornar a matriz atualizada

# Exemplo de uso:
x, y = np.meshgrid(np.arange(-1000, 1000, 1), np.arange(-1000, 1000, 1))
initial_matrix = np.cos(x) + np.cos(y)
updated_matrix = initial_matrix
result = initial_matrix

num_iterations = 5
variacao = 0.1  # Valor pequeno para a variação, menor que 1

# Iniciar o cronômetro
start_time = time.time()

# Parar o cronômetro e exibir o tempo decorrido
updated_matrix = funcao_calor_matrix(updated_matrix, num_iterations, variacao)
elapsed_time = time.time() - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')
#Elapsed time: not optmized

plt.imshow(updated_matrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("Matriz iteração")
plt.show()

# Iniciar o cronômetro
start_time = time.time()

# Executar a função
result = funcao_calor_otim_matrix(result, num_iterations, variacao)

# Parar o cronômetro e exibir o tempo decorrido
elapsed_time = time.time() - start_time
print(f'Elapsed time: {elapsed_time:.4f} seconds')
#Elapsed time: 40 times faster

plt.imshow(result, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("Matriz metodo otimizado")
plt.show()

# Usando uma visualização de calor com matplotlib
if np.allclose(updated_matrix, result, rtol=1e-05, atol=1e-08):
    print("As matrizes são iguais (dentro da tolerância).")
else:
    print("As matrizes são diferentes.")

plt.imshow(updated_matrix - result, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("Diferença entre as matrizes")
plt.show()