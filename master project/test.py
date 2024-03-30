import os
import pandas as pd

def summarize_labels(folder_path, output_folder):
    try:
        # Get a list of files in the specified folder
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

        # Create an empty DataFrame to store the summary for all files
        all_files_summary = pd.DataFrame()

        # Iterate through each CSV file and summarize labels
        for file in files:
            file_path = os.path.join(folder_path, file)

            print(f"\nSummary for {file}:")

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)

            # Check if 'label' column exists
            if 'label' in df.columns:
                # Count occurrences of each label
                label_counts = df['label'].value_counts()

                # Add label counts to the all_files_summary DataFrame
                all_files_summary[file] = label_counts

            else:
                print("\n'Label' column not found in the DataFrame.")

        # Save the combined summary as a CSV file
        combined_summary_filename = os.path.join(output_folder, "combined_label_summary.csv")
        all_files_summary.to_csv(combined_summary_filename, index=True)

        print(f"\nCombined Label Summary saved as {combined_summary_filename}")

    except Exception as e:
        print(f"Error: {e}")

# Replace 'C:\\Users\\Pc\\Desktop\\Masters Project\\Dataset_CICIOT_2023' with the actual path to your folder
folder_path = 'C:\\Users\\Pc\\Desktop\\Masters Project\\Dataset_CICIOT_2023'

# Replace 'C:\\Users\\Pc\\Desktop\\Masters Project\\label_summary_output' with the desired output folder path
output_folder = 'C:\\Users\\Pc\\Desktop\\Masters Project\\label_summary_output'

# Call the function to summarize labels for all CSV files in the folder
summarize_labels(folder_path, output_folder)
