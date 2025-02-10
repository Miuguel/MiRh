import numpy as np

def funcao_calor_otim_matrix(matrix, num_iterations, dt):
    """
    Aplica o método explícito para a simulação do calor em uma matriz.
    usando diferença de matrizes.
    
    :param matriz: Matriz 2D de temperatura inicial (normalizada entre 0 e 1).
    :param num_iteração: Quantas interações devem ser feitas.
    :param dt: .
    :return: Matriz 2D de temperatura final.
    """
    rows, cols = matrix.shape
    for _ in range(num_iterations):
        matrix_up = np.vstack([matrix[1:, :], np.full((1, cols), np.nan)])
        matrix_down = np.vstack([np.full((1, cols), np.nan), matrix[:-1, :]])
        matrix_left = np.hstack([matrix[:, 1:], np.full((rows, 1), np.nan)])
        matrix_right = np.hstack([np.full((rows, 1), np.nan), matrix[:, :-1]])
        
        sum_neighbors = np.nansum(np.stack([matrix_up, matrix_down, matrix_left, matrix_right], axis=0), axis=0)
        num_neighbors = np.sum(~np.isnan(np.stack([matrix_up, matrix_down, matrix_left, matrix_right], axis=0)), axis=0)
        
        new_matrix = matrix + dt * (sum_neighbors / num_neighbors - matrix)
        matrix = new_matrix
    return matrix
