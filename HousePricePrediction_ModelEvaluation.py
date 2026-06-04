# Import Libraries
# Import Pandas for data manipulation and analysis | Pandas is used to handle tabular data (DataFrames)
import pandas as pd
# Import NumPy for numerical and mathematical operations | Numpy handles complex mathematical calculations and arrays
import numpy as np
# Import Matplotlib for data visualization | Matplotlib is used to create plots and charts
import matplotlib.pyplot as plt

# Import scikit-learn for machine learning models | Scikit-learn (sklearn) provides tools for machine learning algorithms
# Split the dataset into training and testing sets
from sklearn.model_selection import train_test_split

# Import the Linear Regression model
from sklearn.linear_model import LinearRegression

# Import metrics to evaluate the model's performance
from sklearn.metrics import (
    mean_absolute_error,  # MAE: Average absolute error
    mean_squared_error,  # MSE: Punishes larger errors more
    r2_score  # R-squared: Variance explained by the model (0 to 1)
)

# Load the dataset into a Pandas DataFrame
df = pd.read_csv('HousePricePrediction.csv')

# Display the first 10 rows
# This helps us understand the structure of the dataset, the types of features, and the target variable (house prices).
# The dataset likely contains features such as 'Size', 'Bedrooms', 'Bathrooms', 'Location', etc., and a target variable like 'Price'.
# By looking at the first 10 rows, we can also check for any missing values or anomalies in the data.
# This step is crucial for data exploration and understanding before we proceed with model training and evaluation.
# The output will show the first 10 rows of the dataset, giving us insight into the features and target variable we will be working with.
# Note: The actual output will depend on the contents of 'HousePricePrediction.csv', but it should display
# a tabular format with columns representing features and rows repr   esenting individual house records.
print("--- First 10 Rows of the Dataset ---")
print(df.head(10))

# Data Analysis (EDA) and Data Cleaning
# a) Display the shape of the dataset
#   This will show us the number of rows (samples) and columns (features) in the dataset.
print("\n--- Dataset Shape ---")
print(df.shape)

# b) Understand the data types of each column and check for missing values
#   This step is important to identify which features are numerical, categorical, or of other types.
#   It also helps us find any missing values that may need to be handled before model training.
# int64 → numeric | float64 → decimal | object → categorical (text) | bool → boolean (True/False)
print("\n--- Data Types ---")
print(df.info())

# Identify missing values
#   This will show the count of missing values in each column. If there are any missing values,
#   we may need to decide how to handle them (e.g., imputation, removal).
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum())

# Generate summary statistics of numerical features
#  This will provide insights into the distribution of numerical features, including measures of
#  central tendency (mean, median) and dispersion (standard deviation, min, max).
print("\n--- Summary Statistics ---")
print(df.describe())

# Check the distribution of the target variable (house prices)
#   This will help us understand if the target variable is normally distributed or skewed.
print("\n--- Skewness of SalePrice ---")
print(df['SalePrice'].skew())

# Data Cleaning
# Create a copy to store the clean data
df_filled = df.copy()
# Remove rows where target variable is missing
df_filled = df_filled[df_filled['SalePrice'].notnull()].copy()

# Handle missing values by filling them with the mean of the respective columns
# This is a common imputation technique for numerical features, where we replace missing values with the average value of that feature.
# df_filled.fillna(df_filled.mean(), inplace=True)

# Smart filling: Numbers get the middle value, Text gets the most common value
# The reason we use a loop instead of a single command like df.mean() is because
# our dataset is mixed data types. Some columns are numbers, and others are words.

# Check if dataset has any missing values
if df_filled.isnull().sum().sum() > 0:
    print("Missing values found. Cleaning data...")

    # Special handling: missing basement area means no basement
    basement_cols = ['BsmtFinSF2', 'TotalBsmtSF']

    for col in basement_cols:
        if col in df_filled.columns:
            df_filled[col] = df_filled[col].fillna(0)

    # General handling
    for col in df_filled.columns:
        # Do not fill target column, as it may have missing values that we want to predict
        if col == 'SalePrice':
            continue

        # Skip columns already handled
        if col in basement_cols:
            continue

        if df_filled[col].dtype == 'object':
            # Text columns
            df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
        else:
            # Numeric columns
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())

    print("Missing values handled successfully.")
else:
    print("No missing values found. No cleaning needed.")

# Verify that there are no missing values left
print("\n--- Missing Values After Smart Filling ---")
print(df_filled.isnull().sum())
print("\n--- Data Info After Cleaning ---")
print(df_filled.info())


# Check and remove duplicate records if any
duplicate_count = df_filled.duplicated().sum()
print(f"\nDuplicates found: {duplicate_count}")
if duplicate_count > 0:
    df_filled.drop_duplicates(inplace=True)
    print(f"Duplicates removed. Current dataset shape: {df_filled.shape}")

# Feature selection
# First, remove unnecessary columns (like Id) so they aren't included in features
df_filled.drop(columns=['Id'], axis=1, inplace=True, errors='ignore')
print("\nColumn 'Id' has been removed.")

# Select relevant features for prediction and separate the target variable
# Assuming 'SalePrice' is the target variable and the rest are features
# We drop the target variable "SalePrice" from the features list to ensure
# that we only use the relevant features for model training.
target = 'SalePrice'
features = df_filled.columns.drop(target)
print("\n--- Selected Features ---")
print(features)
print("\n--- Target Variable ---")
print(target)

CHECK THIS OUT LATER
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
