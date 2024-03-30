import pandas as pd
import numpy as np
 
# Load data
df = pd.read_csv("C:\\Users\\Pc\\Desktop\\Masters Project\\Dataset_CICIOT_2023\\part-00025-363d1ba3-8ab5-4f96-bc25-4d5862db7cb9-c000.csv")
 
df.head()
df.shape

# To clear first 10columns
df = df.iloc[:,:10]
df.head()


# Missing values
missing_count = df.isnull().sum()
missing_count

# Total of missing values
total_cells = np.product(df.shape)
total_missing = df.isnull().sum().sum()
 
# Percentage of missing data
(total_missing/total_cells) * 100


# Remove all columns with at least one missing value
new_df = df.dropna(axis=1)
new_df.head()


# Data loss
print("Number of columns in the original dataset: %d \n" % df.shape[1])
print("Number of columns with NaN values removed: %d" % new_df.shape[1])
 
# Output
# Number of columns in the original dataset: 10
# Number of columns with NaN values removed: 5


# Replace missing values with 0
df = df.fillna(0)
df.head()