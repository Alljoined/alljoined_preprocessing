# alljoined_preprocessing

## Folder Structure
Below is a description of the main files and directories:

    ├── eeg_data/                # Data file (Add this)
    │   ├── before/            
            ├── sub-01
                ├── ses-01  
                    ├── sub-01_ses-01_raw.csv  # Add .csv file before processing here
    │   └── after/           
            ├── sub-01
                ├── ses-01  
                    ├── sub-01_ses-01_raw.csv # Where processed .csv will be saved to
    ├── process_cell.py 
    └── README.md           # The file you're reading now