# 1. Dataset Loading
# Load the dataset into a Pandas DataFrame
# Display the first 10 rows
# Import pandas library
import pandas as pd

# Load the dataset into a Pandas DataFrame
df = pd.read_csv('HousePricePrediction.csv')

# Display the first 10 rows
print("--- First 10 Rows of the Dataset ---")
print(df.head(10))

# 2.  Data Exploration
# Display the shape of the dataset
print("\n--- Dataset Shape ---")
print(df.shape)

# Check data types of all columns
print("\n--- Data Types ---")
print(df.dtypes)

# Generate summary statistics of numerical features
print("\n--- Summary Statistics ---")
print(df.describe())

# Identify missing values
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum())

# 3. Data Cleaning
# Handle missing values by filling them with the mean of the respective columns
# Fill missing values with the mean of the respective columns

# Create a copy to store the clean data
df_filled = df.copy()

# Smart filling: Numbers get the middle value, Text gets the most common value
# The reason we use a loop instead of a single command like df.mean() is because
# our dataset is mixed data types. Some columns are numbers, and others are words.
for col in df_filled.columns:
    if df_filled[col].dtype == 'object':
        # Text columns
        df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
    else:
        # Numeric columns
        df_filled[col] = df_filled[col].fillna(df_filled[col].median())
# Verify that there are no missing values left
print("\n--- Missing Values After Smart Filling ---")
print(df_filled.isnull().sum())

# Check and remove duplicate records if any
duplicate_count = df_filled.duplicated().sum()
print(f"\nDuplicates found: {duplicate_count}")
df_filled.drop_duplicates(inplace=True)
print(f"Duplicates removed. Current dataset shape: {df_filled.shape}")

# 4. Feature selection
# First, remove unnecessary columns (like Id) so they aren't included in features
df_filled.drop(columns=['Id'], axis=1, inplace=True, errors='ignore')
print("\nColumn 'Id' has been removed.")

# Select relevant features for prediction and separate the target variable
# Assuming 'SalePrice' is the target variable and the rest are features
target = 'SalePrice'
features = df_filled.columns.drop(target)
print("\n--- Selected Features ---")
print(features)
print("\n--- Target Variable ---")
print(target)

# 5. Data Preprocessing
# Encode categorical variables using one-hot encoding
# Identify categorical columns
categorical_cols = df_filled.select_dtypes(include=['object']).columns
print("\n--- Categorical Columns ---")
print(categorical_cols)

# Convert categorical variables into numerical form (One-Hot Encoding)
# We use drop_first=True to avoid the "dummy variable trap" (mathematical redundancy)
df_encoded = pd.get_dummies(
    df_filled, columns=categorical_cols, drop_first=True)
print("\n--- Dataset After One-Hot Encoding ---")
print(df_encoded.head())

# Display the preview of the final dataset
print("\n--- Final Preprocessed Dataset Preview ---")
print(df_encoded.head())

# Print new shape
print(f"\nNew Shape: {df_encoded.shape}")
