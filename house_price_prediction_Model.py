# STEP 1: Import Libraries
# Import Pandas for data (DataFrames) manipulation and analysis.
import pandas as pd

# Import NumPy for numerical and mathematical operations and handling arrays.
import numpy as np

# Import Matplotlib for data visualization and plotting charts.
import matplotlib.pyplot as plt

# Import Seaborn for statistical data visualization and creating attractive graphics.
import seaborn as sns

# Import Scikit-learn (sklearn) for machine learning models
# Split the dataset into training and testing sets
from sklearn.model_selection import train_test_split

# Import the Linear Regression model
from sklearn.linear_model import LinearRegression

# Import metrics to evaluate the model's performance
from sklearn.metrics import (
    mean_absolute_error,        # MAE: Average absolute error
    mean_squared_error,         # MSE: Punishes larger errors more
    # R-squared: Variance explained by the model (0 to 1)
    r2_score
)

# Import LabelEncoder for encoding categorical variables
# LabelEncoder converts categorical text data into numerical labels, which is necessary
# for machine learning algorithms that require numerical input.
# from sklearn.preprocessing import LabelEncoder

# Pretty formatting
pd.set_option("display.max_columns", 20)
pd.set_option("display.width",       120)
sns.set_theme(style="whitegrid", palette="muted")

print("=" * 60)
print("STEP 2 — LOAD & INSPECT THE DATASET")
print("=" * 60)

# STEP 2: Load & Inspect the Data
# Load the dataset into a Pandas DataFrame
df = pd.read_csv('HousePricePrediction.csv')

# Display the first 10 rows of the dataset to get an initial understanding
# of the data structure, features, and target variable.
print("First 10 rows:")
print(df.head(10))

# ── STEP 2B: Understand Each Column ───────────────────────────
# Not requried in actual program but we can keep it if required.
# Display the last 10 rows of the dataset to check for any anomalies or patterns
print("\n\n" + "=" * 60)
print("STEP 2b — COLUMN DESCRIPTIONS")
print("=" * 60)

col_info = {
    "Id": "Row identifier (not a real feature)",
    "MSSubClass": "Building class (20=1-story, 60=2-story, etc.)",
    "MSZoning": "Zoning classification (RL=Residential Low, etc.)",
    "LotArea": "Lot size in square feet",
    "LotConfig": "Lot shape / configuration",
    "BldgType": "Type of dwelling (1Fam, TwnhsE, etc.)",
    "OverallCond": "Overall condition rating (1–10)",
    "YearBuilt": "Original construction year",
    "YearRemodAdd": "Remodel year (same as YearBuilt if none)",
    "Exterior1st": "Exterior covering on house",
    "BsmtFinSF2": "Type 2 finished basement area (sq ft)",
    "TotalBsmtSF": "Total basement area (sq ft)",
    "SalePrice": "★ TARGET — Property sale price in $",
}
for col, desc in col_info.items():
    dtype = df[col].dtype
    print(f"  {col:<14} [{dtype}]  → {desc}")

# STEP 3: Data Analysis (EDA)
# a) Display the shape of the dataset / # rows (samples): columns (features) in the dataset.
print("\n\n" + "=" * 60)
print("STEP 3 — EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# b) Understand the data types of each column | Identify numerical, categorical, and other types of features.
# This is crucial for selecting appropriate preprocessing steps and machine learning algorithms.
# int64 → numeric | float64 → decimal | object → categorical (text) | bool → boolean (True/False)
print("\n--- Data Types ---")
print(df.info())

# c) Check for missing values in the dataset and their counts.
# Missing values can lead to biased models or errors during training,
# so it's important to identify and handle them appropriately and decide on a strategy
# (e.g., imputation, removal) based on the extent and nature of the missing data.
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum())
# missing_counts = df.isnull().sum()
# missing = missing_counts[missing_counts > 0]
# print(missing)

# d) Generate summary statistics for numerical features to understand
# data distribution, central tendency, spread, and detect possible outliers.
print("\n--- Summary Statistics ---")
print(df.describe())

# e) Analyze the distribution of the target variable (house prices)- This analysis helps us understand
# the nature of the target variable and informs our modeling approach.
print("\n--- Skewness of SalePrice ---")
print(df['SalePrice'].skew())

# A skewness value greater than 1 or less than -1 indicates a highly skewed distribution,
# which may require transformation (e.g., log transformation) to improve model performance.

# f) Visualize the distribution of the target variable (SalePrice) using a histogram and boxplot.
# The histogram shows the frequency distribution of house prices, while the boxplot helps identify
# outliers and the overall spread of the data.
print("\n--- Distribution of SalePrice ---")
# Width = 12 inches; Height = 5 inches
# Set the figure size for better visibility of the plots
plt.figure(figsize=(12, 5))
# Create a subplot for the histogram (1 row, 2 columns, 1st plot)
plt.subplot(1, 2, 1)
# Plot a histogram with a kernel density estimate (KDE) to show the distribution of SalePrice
# KDE provides a smoothed curve that represents the probability density function of the data,
# while bins=30 divides the data into 30 intervals for the histogram.
sns.histplot(df['SalePrice'], kde=True, bins=30)
plt.title('Distribution of SalePrice')
# Create a subplot for the boxplot (1 row, 2 columns, 2nd plot)
plt.subplot(1, 2, 2)
# Plot a boxplot to visualize the spread and identify outliers in SalePrice
sns.boxplot(x=df['SalePrice'])
plt.title('Boxplot of SalePrice')
plt.tight_layout()              # Adjust the layout to prevent overlapping
plt.show()

# STEP 4: Pre-Processing
print("\n\n" + "=" * 60)
print("STEP 4 — PRE-PROCESSING")
print("=" * 60)
# a) Handle missing values and keep only labelled rows (where SalePrice is known).
df_labelled = df.dropna(subset=["SalePrice"]).copy()
print(f"\n Rows with known SalePrice: {len(df_labelled):,}")

# 4b. Drop the Id column — it's just a row number and not a feature
if "Id" in df_labelled.columns:
    df_labelled.drop(columns=["Id"], inplace=True)
print(df_labelled.head(3))

# 4c. Check for any remaining missing values in the labelled dataset.
print("\n--- Missing Values in Labelled Dataset ---")
missing_values = df_labelled.isnull().sum()
missing_values = missing_values[missing_values > 0]
print(missing_values.sort_values(ascending=False))

# 4d. Remove duplicates in the labelled dataset.
print("\n--- Duplicate Values in Labelled Dataset ---")
duplicate_count = df_labelled.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")
if duplicate_count > 0:
    df_labelled.drop_duplicates(inplace=True)
    print(f"Duplicates removed. Current dataset shape: {df_labelled .shape}")

# 4e. Separate numerical and categorical columns
categorical_cols = df_labelled.select_dtypes(include="object").columns.tolist()
print(f"\n Categorical columns to encode: {categorical_cols}")

numerical_cols = df_labelled.select_dtypes(
    include=[np.number]).columns.tolist()
print(f"\n Numerical columns to impute: {numerical_cols}"
      )
# Exclude target column from feature processing
numerical_cols.remove("SalePrice")   # don't impute the target

# Check if missing values exist
total_missing_count = df_labelled.isnull().sum().sum()

if total_missing_count > 0:
    print(f"\n Missing values found: {total_missing_count}")

    # 4f. Fill missing numerical values with median
    df_labelled[numerical_cols] = df_labelled[numerical_cols].fillna(
        df_labelled[numerical_cols].median()
    )

    # 4g. Fill missing categorical values with mode
    for col in categorical_cols:
        df_labelled[col] = df_labelled[col].fillna(
            df_labelled[col].mode()[0]
        )

    # 4h. Validate after filled missing values
    remaining_missing_count = df_labelled.isnull().sum().sum()
    print(
        f"Remaining missing values after filled missed values: {remaining_missing_count}")

    if remaining_missing_count == 0:
        print("Missing values handled successfully.")
    else:
        print("Warning: Some missing values still remain.")

else:
    print("\nNo missing values found. Skipping imputation.")

print("\nPre-processing complete. Remaining NaN:",
      df_labelled.isnull().sum().sum())

# 4i. Check duplicate rows
duplicate_count = df_labelled.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")

if duplicate_count > 0:

    # Remove duplicates
    df_labelled.drop_duplicates(inplace=True)

    # Validate duplicates after removal
    remaining_duplicates = df_labelled.duplicated().sum()

    print(f"Remaining duplicate rows: {remaining_duplicates}")

    if remaining_duplicates == 0:
        print("Duplicates removed successfully.")
    else:
        print("Warning: Some duplicates still remain.")

else:
    print("No duplicate rows found.")

# 4j. Encode categorical variables using one-hot encoding
df_encoded = pd.get_dummies(
    df_labelled,
    columns=categorical_cols,
    drop_first=True
)
print("\nCategorical variables encoded successfully.")
print(f"Encoded dataset shape: {df_encoded.shape}")
print("\n--- Dataset Info After Encoding ---")
print(df_encoded.info())

# 4k. Separate features (X) and target (y)
# The feature matrix X contains all the independent variables (features) used to predict the target variable,
# while the target vector y contains the dependent variable (SalePrice) that we want to predict.
# axis=0 ==> rows, axis=1 ==> columns
X = df_encoded.drop(columns=["SalePrice"], axis=1)
y = df_encoded["SalePrice"]

print("\nFeatures and target variable separated successfully.")
print(f"Feature X dataset shape: {X.shape}")
print(f"Target y dataset shape: {y.shape}")

# STEP 5: Train-Test Split
# The train-test split is a crucial step in machine learning to evaluate the performance of a model on unseen data.
# By splitting the dataset into a training set and a test set,
# we can train the model on the training data and then evaluate its performance on the test data,
# which simulates how the model would perform in real-world scenarios where it encounters new, unseen data.
print("\n\n" + "=" * 60)
print("STEP 5 — TRAIN-TEST SPLIT (80 / 20)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,    # 20 % for testing
    # stratify   = y,       # stratified sampling to maintain target distribution
    # random_state ensures reproducible train-test splits across multiple runs.
    random_state=42       # fixed seed → reproducible results
)

print(
    f"\n Training samples : {len(X_train):,}  ({len(X_train)/len(X)*100:.0f}%)")
print(f" Testing  samples : {len(X_test):,}   ({len(X_test)/len(X)*100:.0f}%)")

# Training the model involves fitting it to the training data, which allows it to learn the
# relationships between the features and the target variable.
# Evaluating the model's performance on the test data provides an unbiased estimate of how well
# the model generalizes to new, unseen data, which is crucial for assessing its real-world applicability
# and effectiveness.

# In this step, we will train a Linear Regression model, which is a simple and widely used
# algorithm for regression tasks.

# Linear Regression assumes a linear relationship between the features and the target variable,
# making it a good starting point for predicting house prices based on the features in our dataset.
# The model will learn coefficients for each feature that indicate how much that feature contributes
# to the predicted house price.

# After training the model, we will evaluate its performance using metrics such as
# Mean Absolute Error (MAE),Mean Squared Error (MSE), and R-squared (R²) to understand how
# well the model is performing and to identify areas for improvement.
# The evaluation metrics will help us assess the accuracy of our predictions and the overall
# fit of the model to the data.

# Note: In a real-world scenario, we would also consider more complex models and perform hyperparameter tuning
# to further improve performance, but for this exercise, we will focus on training a simple Linear
# Regression model as a baseline.
# TERMINOLOGY
# LinearRegression() — an Ordinary Least Squares (OLS) model that
#                      finds coefficients minimising Σ(actual - predicted)²
# .fit(X_train, y_train) — the 'learning' step; model reads the training
#                           data and adjusts its internal coefficients

# STEP 6: Train the model on the training data and evaluate its performance on the test data.
print("\n\n" + "=" * 60)
print("STEP 6 — TRAINING THE LINEAR REGRESSION MODEL")
print("=" * 60)

# Create Linear Regression model instance
model = LinearRegression()
# Train model using training data (X_train, y_train)
model.fit(X_train, y_train)

print("\n Model trained successfully!")

# Display intercept and coefficients
print(f"\n  Intercept (β0)  : ${model.intercept_:,.2f}")
print("\n  Feature Coefficients (impact on predicted SalePrice)::")

# Display feature coefficients
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_}).sort_values("Coefficient", ascending=False)
# print(coef_df.to_string(index=False))
print("\nTop 10 Positive Features:")
print(coef_df.head(10).to_string(index=False))

print("\nTop 10 Negative Features:")
print(coef_df.tail(10).to_string(index=False))
# A positive coefficient means: as that feature increases, price increases-while keeping other variables constant.
# A negative coefficient means: as that feature increases, price decreases-while keeping other variables constant.

# STEP 7: Model Prediction
# After training the model, we will use it to make predictions on the test set (X_test) and compare
# the predicted house prices with the actual house prices (y_test) to evaluate the model's performance.
# The predictions will help us understand how well the model generalizes to new, unseen data and
# identify any discrepancies between predicted and actual values.
# We will also create a comparison table to visualize the first 10 predictions alongside the actual
# values and their differences, which can provide insights into the model's accuracy and areas where
# it may be underperforming.
# The evaluation of the model's predictions will be crucial for determining its effectiveness and g
# guiding any necessary improvements or adjustments to the model or the features used for prediction.
# TERMINOLOGY
# .predict(X_test) — uses the trained model to predict target values for the test features
# y_pred — the predicted house prices generated by the model for the test set
# comparison DataFrame — a table that compares the actual house prices (y_test) with the predicted
# house prices (y_pred) and calculates the difference between them to evaluate the model's performance.
#
# Note: In a real-world scenario, we would also calculate and display evaluation metrics such as MAE, MSE, and R²
# to quantitatively assess the model's performance, but for this exercise, we will focus on
# generating predictions and comparing them to actual values in a tabular format.

# STEP 7: Model Prediction
print("\n\n" + "=" * 60)
print("STEP 7 — Model Prediction and Comparison")
print("=" * 60)

y_pred = model.predict(X_test)

# Preview first 10 predictions vs actuals
comparison = pd.DataFrame({
    "Actual ($)": y_test.values[:10],
    "Predicted ($)": y_pred[:10].round(0),
    "Difference ($)": (y_test.values[:10] - y_pred[:10]).round(0)
})
print("\n📋 First 10 Predictions vs Actual:")
print(comparison.to_string(index=False))
# The comparison table shows the actual house prices, the predicted house prices generated by the model,
# and the difference between the actual and predicted values for the first 10 samples in the test set.
# This allows us to visually assess how well the model is performing on individual predictions and identify
# any significant discrepancies that may indicate areas for improvement in the model or the features used
# for prediction.
# Positive difference : Model predicted HIGHER than actual price.
# Negative difference : Model predicted LOWER than actual price.

# STEP 8: Model Evaluation================
# After generating predictions, we will evaluate the model's performance using several key metrics:
# 1. Mean Absolute Error (MAE): This metric calculates the average absolute difference between the actual
#    house prices and the predicted house prices. It provides a straightforward measure of the average error
#    in the same units as the target variable (dollars). A lower MAE indicates better model performance.
# 2. Mean Squared Error (MSE): This metric calculates the average of the squared differences between the actual
#    house prices and the predicted house prices. MSE penalizes larger errors more than smaller
#    errors, making it sensitive to outliers. A lower MSE indicates better model performance.
# 3. Root Mean Squared Error (RMSE): This is the square root of the MSE and provides an error metric in the
#    same units as the target variable (dollars). RMSE is also sensitive to out
#    liers and provides a more interpretable measure of the average error. A lower RMSE indicates better model performance.
# 4. R-squared (R²): This metric represents the proportion of the variance in the target variable that is
#    explained by the model. R² values range from 0 to 1, where
#    - An R² of 0 indicates that the model does not explain any of the variance in the target variable.
#    - An R² of 1 indicates that the model explains all the variance in the target variable.
#    A higher R² indicates better model performance, with values closer to 1 indicating a
#    better fit of the model to the data.
# STEP 8: Model Evaluation
print("\n\n" + "=" * 60)
print("STEP 8 — MODEL EVALUATION METRICS")
print("=" * 60)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Create evaluation table
evaluation_df = pd.DataFrame({
    "Metric": ["MAE", "MSE", "RMSE", "R² Score"],
    "Value": [
        round(mae, 2),
        round(mse, 2),
        round(rmse, 2),
        round(r2, 4)
    ]
})

print("\n Model Evaluation Metrics:")
print(evaluation_df.to_string(index=False))
# Note on scientific notation: 3.412285e+04 simply means 3.412285 × 10⁴ = 34,122.85.
# Python uses this format when numbers are very large or very small.
