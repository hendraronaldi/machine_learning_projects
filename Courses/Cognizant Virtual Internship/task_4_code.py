import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

# global variables

# training size for train test split size
SPLIT = 0.75

# cross validation K fold
K = 10

# csv data path
DATA_PATH = 'merged_stock_levels.csv'

# target column name
TARGET = 'estimated_stock_pct'

# load_dataset function to load csv dataset in pandas dataframe format
def load_dataset(path: str='path/to/csv'):
    df = pd.read_csv(path)
    df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
    return df

# extract_feature_target to get features (X) and target (y) from dataframe
def extract_feature_target(df: pd.DataFrame = None, target: str = "estimated_stock_pct"):
    if target not in df.columns:
        raise Exception(f"Target: {target} is not present in the data")
    
    X = df.drop(columns=[target])
    y = df[target]
    return X, y

# model_training_cross_validation
def model_training_cross_validation(X, y, split: 0.75, K: 10):
    maes = []

    for fold in range(0, K):

        # Instantiate algorithm
        model = RandomForestRegressor()
        scaler = StandardScaler()

        # Create training and test samples
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=split)

        # Scale X data, we scale the data because it helps the algorithm to converge
        # and helps the algorithm to not be greedy with large values
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        # Train model
        trained_model = model.fit(X_train, y_train)

        # Generate predictions on test sample
        y_pred = trained_model.predict(X_test)

        # Compute accuracy, using mean absolute error
        mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
        maes.append(mae)
        print(f"Fold {fold + 1}: MAE = {mae:.3f}")

    print(f"Average MAE: {(sum(maes) / len(maes)):.2f}")


# example run code
def run():
    df = load_dataset(DATA_PATH)
    X, y = extract_feature_target(df, TARGET)
    model_training_cross_validation(X, y, SPLIT, K)