% Read the table from the CSV file, change #
T = readtable('sub-0#_ses-0#_preletswave.csv')

% Directly create a cell array from the selected columns of the table
events = table2cell(T(:, 1:3));

% Clear all variables except 'events'
clearvars -except events