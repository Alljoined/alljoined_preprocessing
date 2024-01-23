import pandas as pd

# Define the file paths
input_file_path = 'eeg_data/after/sub-01/ses-01/sub-06_ses-01_preletswave.csv'
output_file_path = 'eeg_data/after/sub-01/ses-01/modified_sub-06_ses-01_preletswave.csv'

# Load the CSV file
df = pd.read_csv(input_file_path)

# Create a list to mark rows for deletion
rows_to_delete = []

# Iterate through the DataFrame
for i in range(len(df) - 1):
    # Check if the current row's 'code' is 252
    if df.at[i, 'code'] == 252:
        rows_to_delete.append(i)
    # Check if the next row's 'code' is not 252 or 253
    elif df.at[i + 1, 'code'] not in [252, 253]:
        rows_to_delete.append(i)

# Drop the rows
df.drop(rows_to_delete, inplace=True)

# Save to a new CSV file
df.to_csv(output_file_path, index=False)
