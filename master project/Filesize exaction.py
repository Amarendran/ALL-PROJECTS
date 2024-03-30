import os
import pandas as pd

def get_csv_files_size(folder_path):
    file_sizes = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
                file_sizes[file] = file_size

    return file_sizes

# Provide the path to your folder containing CSV files
folder_path = r'C:\Users\Pc\Desktop\Masters Project\Dataset_CICIOT_2023'
file_sizes = get_csv_files_size(folder_path)

# Create a pandas DataFrame
df = pd.DataFrame(list(file_sizes.items()), columns=['File Name', 'Size (MB)'])

# Calculate and append the total file size as the last row
total_size_mb = df['Size (MB)'].sum()

# Create a new DataFrame for the 'Total' row
total_row = pd.DataFrame({'File Name': ['Total'], 'Size (MB)': [total_size_mb]})

# Concatenate the original DataFrame and the 'Total' row
df = pd.concat([df, total_row], ignore_index=True)

# Specify the CSV file path to save the data
output_folder = r'C:\Users\Pc\Desktop\Masters Project\label_summary_output'
csv_file_path = os.path.join(output_folder, 'file_sizes_pandas_with_total.csv')

# Check if the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print(f"The file sizes with the total have been saved to: {csv_file_path}")
