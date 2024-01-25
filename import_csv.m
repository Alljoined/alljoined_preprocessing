newTable = readtable("Sub06.csv");
dataTable = newTable(:, [1:3]);

% Convert the table to a cell array of character vectors
cellArray = cell(size(dataTable));
for i = 1:size(dataTable, 1)
    for j = 1:size(dataTable, 2)
        if j == 1 
            cellArray{i, j} = num2str(dataTable{i, j});
        else
            cellArray{i, j} = table2array(dataTable(i, j));
        end
    end
end
 
events = cellArray;