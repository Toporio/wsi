import numpy as np


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value


class CartTree:
    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None

    def calculate_gini_impurity(self, y):
        """
        evaluate value of gini impurity of vector of y
        vector has to be discretized
        """
        classes, counts = np.unique(y.flatten(), return_counts=True)
        if len(counts) == 0:
            return 0
        n_samples = np.sum(counts)
        gini = 1.0
        for count in counts:
            p_i = count / n_samples
            gini -= p_i**2
        return gini

    def split(self, X, y):
        n_samples, n_features = X.shape
        parent_impurity = self.calculate_gini_impurity(y)
        best_gain = -1
        best_feature = None
        best_threshold = None
        for feature in range(n_features):
            X_col = X[:, feature]
            thresholds = np.percentile(X_col, np.linspace(0, 100, num=10))
            thresholds = np.unique(thresholds)
            for threshold in thresholds:
                left_indices = X_col <= threshold
                right_indices = X_col > threshold

                if (
                    np.sum(left_indices) < self.min_samples_leaf
                    or np.sum(right_indices) < self.min_samples_leaf
                ):
                    continue

                y_left, y_right = y[left_indices], y[right_indices]
                n_left, n_right = len(y_left), len(y_right)
                left_gini = self.calculate_gini_impurity(y_left)
                right_gini = self.calculate_gini_impurity(y_right)
                gain = (
                    parent_impurity
                    - (n_left / n_samples) * left_gini
                    - (n_right / n_samples) * right_gini
                )
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold

    def build_tree(self, X, y, depth=0):
        n_samples, _ = X.shape
        n_labels = len(np.unique(y))
        if (
            (self.max_depth is not None and depth >= self.max_depth)
            or n_labels == 1
            or n_samples < self.min_samples_split
        ):
            return Node(value=self.most_common_label(y))
        feature, threshold = self.split(X, y)
        if feature is None:
            return Node(value=self.most_common_label(y))
        left_indices = X[:, feature] <= threshold
        right_indices = X[:, feature] > threshold
        left_child = self.build_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self.build_tree(X[right_indices], y[right_indices], depth + 1)
        return Node(
            feature=feature, threshold=threshold, left=left_child, right=right_child
        )

    def fit(self, X, y):
        self.root = self.build_tree(X, y)

    def predict_single(self, x):
        node = self.root
        while node.left is not None:
            if x[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

    def predict(self, X):
        return np.array([self.predict_single(x) for x in X])

    def most_common_label(self, y):
        counts = np.bincount(y)
        return int(np.argmax(counts))
