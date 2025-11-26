import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import KBinsDiscretizer
from ucimlrepo import fetch_ucirepo

"""`
Data preprocessing for wine quality dataset.
"""
wine_quality = fetch_ucirepo(id=186)
X = wine_quality.data.features
Y = wine_quality.data.targets

# If wine quality is greater than 5, set to 1, otherwise 0.
Y_bin = (Y["quality"] > 5).astype(int).values.reshape(-1, 1)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y_bin, test_size=0.25, random_state=42
)
print("X_train:", X_train.shape)
print("Y_train:", type(Y_train))
print("X_test:", X_test.shape)
print("Y_test:", Y_test.shape)
