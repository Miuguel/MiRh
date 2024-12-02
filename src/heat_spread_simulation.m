function updated_matrix_lacos = update_matrix_lacos(matrix, num_iterations, variacao)
    % Função para atualizar a matriz
    % matrix: matriz inicial
    % num_iterations: número de iterações
    % variacao: delta x

    [rows, cols] = size(matrix); % Tamanho da matriz

    for iter = 1:num_iterations
        new_matrix = matrix; % Cópia da matriz original para atualizar valores

        for i = 1:rows
            for j = 1:cols
                % Calcular a soma dos vizinhos adjacentes
                sum_neighbors = 0;
                num_neighbors = 0;

                if i > 1
                    sum_neighbors = sum_neighbors + matrix(i-1, j); % Célula acima
                    num_neighbors = num_neighbors + 1;
                end

                if i < rows
                    sum_neighbors = sum_neighbors + matrix(i+1, j); % Célula abaixo
                    num_neighbors = num_neighbors + 1;
                end

                if j > 1
                    sum_neighbors = sum_neighbors + matrix(i, j-1); % Célula à esquerda
                    num_neighbors = num_neighbors + 1;
                end
 
                if j < cols
                    sum_neighbors = sum_neighbors + matrix(i, j+1); % Célula à direita
                    num_neighbors = num_neighbors + 1;
                end

                % Atualizar a célula atual baseada na média dos vizinhos
                if num_neighbors > 0
                    new_matrix(i, j) = matrix(i, j) + variacao*(sum_neighbors / num_neighbors - matrix(i,j));
                end
            end
        end

        matrix = new_matrix; % Atualizar a matriz original com a nova matriz
    end

    updated_matrix_lacos = matrix; % Retornar a matriz atualizada
end

% Exemplo de uso: z = 1./x + 1./y
%2k por 2k é o limite
[x,y]=meshgrid(-0.5:0.0005:0.5,-0.5:0.0005:0.5);
initial_matrix = cos(x) + cos(y);
num_iterations = 5;
variacao = 0.1; % Valor pequeno para a variação

% Iniciar o cronômetro
tic;

% Executar a função
result = update_matrix_lacos(initial_matrix, num_iterations, variacao);

% Parar o cronômetro e exibir o tempo decorrido
elapsed_time = toc;
disp('Updated Matrix:');
%mesh(x, y, result);
fprintf('Elapsed time: %.4f seconds\n', elapsed_time);