function updated_matrix_otim = update_matrix_otim(matrix, num_iterations, variacao)
    % Função para atualizar a matriz
    % matrix: matriz inicial
    % num_iterations: número de iterações
    % variacao: fator de variação pequeno

    [rows, cols] = size(matrix); % Tamanho da matriz

    for iter = 1:num_iterations
        % Criar matrizes deslocadas
        matrix_up = [matrix(2:end, :); zeros(1, cols)];
        matrix_down = [zeros(1, cols); matrix(1:end-1, :)];
        matrix_left = [matrix(:, 2:end) zeros(rows, 1)];
        matrix_right = [zeros(rows, 1) matrix(:, 1:end-1)];
        
        % Soma das matrizes deslocadas
        sum_neighbors = matrix_up + matrix_down + matrix_left + matrix_right;
        
        % Número de vizinhos válidos
        num_neighbors = (matrix_up ~= 0) + (matrix_down ~= 0) + (matrix_left ~= 0) + (matrix_right ~= 0);
        
        % Evitar divisão por zero
        num_neighbors(num_neighbors == 0) = 1;
        
        % Calcular a nova matriz com a fórmula fornecida
        new_matrix = matrix + variacao * (sum_neighbors ./ num_neighbors - matrix);
        
        % Atualizar a matriz original com a nova matriz
        matrix = new_matrix;
    end

    updated_matrix_otim = matrix; % Retornar a matriz atualizada
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
result = update_matrix_otim(initial_matrix, num_iterations, variacao);

% Parar o cronômetro e exibir o tempo decorrido
elapsed_time = toc;
disp('Updated Matrix:');
%mesh(x, y, result);
fprintf('Elapsed time: %.4f seconds\n', elapsed_time);

%
%
%