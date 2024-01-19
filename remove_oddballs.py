import pandas as pd

# Define the file paths
input_file_path = 'eeg_data/after/sub-01/ses-01/sub-01_ses-01_preletswave.csv'
output_file_path = 'eeg_data/after/sub-01/ses-01/sub-01_ses-01_preletswave.csv'

# Load the CSV file
df = pd.read_csv(input_file_path)

# Create a list to mark rows for deletion
rows_to_delete = []

# Iterate through the DataFrame
for i in range(1, len(df)):
    if df.at[i, 'code'] in [254, 251]:
        rows_to_delete.extend([i-1, i])

# Remove duplicates from the list
rows_to_delete = list(set(rows_to_delete))

# Debugging: Print the rows to be deleted
print(f"Rows to delete: {rows_to_delete}")

# Drop the rows
df.drop(rows_to_delete, inplace=True)

# Save to a new CSV file
df.to_csv(output_file_path, index=False)
