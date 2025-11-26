import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

from cart_tree import CartTree
from data import X_test, X_train, Y_test, Y_train


def run_experiment():
    X_train_np = np.array(X_train) if hasattr(X_train, "values") else X_train
    X_test_np = np.array(X_test) if hasattr(X_test, "values") else X_test
    y_train_flat = Y_train.ravel()
    y_test_flat = Y_test.ravel()
    # Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_np)
    X_test_scaled = scaler.transform(X_test_np)
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_scaled, y_train_flat)
    y_pred_lr = log_reg.predict(X_test_scaled)
    acc_lr = accuracy_score(y_test_flat, y_pred_lr)
    print(f"Logistic Regression Accuracy: {acc_lr:.4f}")

    # 3. Analyst of  max_depth for decision tree
    depths = range(1, 21)
    train_scores_depth = []
    test_scores_depth = []
    for d in depths:
        tree = CartTree(max_depth=d, min_samples_split=10, min_samples_leaf=5)
        tree.fit(X_train_np, y_train_flat)
        # predictions
        train_pred = tree.predict(X_train_np)
        test_pred = tree.predict(X_test_np)

        # scores
        acc_train = accuracy_score(y_train_flat, train_pred)
        acc_test = accuracy_score(y_test_flat, test_pred)
        train_scores_depth.append(acc_train)
        test_scores_depth.append(acc_test)
        print(f"Depth: {d:<2} | Train Acc: {acc_train:.4f} | Test Acc: {acc_test:.4f}")

    # Finding best max depth
    best_depth_idx = np.argmax(test_scores_depth)
    best_depth = depths[best_depth_idx]
    best_acc_tree = test_scores_depth[best_depth_idx]
    print(f"\nBest tree: Depth={best_depth}, Accuracy={best_acc_tree:.4f}")

    splits = [2, 5, 10, 20, 40, 60, 100, 150, 200]
    train_scores_split = []
    test_scores_split = []

    for s in splits:
        tree = CartTree(max_depth=best_depth, min_samples_split=s, min_samples_leaf=5)
        tree.fit(X_train_np, y_train_flat)

        train_pred = tree.predict(X_train_np)
        test_pred = tree.predict(X_test_np)

        acc_train = accuracy_score(y_train_flat, train_pred)
        acc_test = accuracy_score(y_test_flat, test_pred)

        train_scores_split.append(acc_train)
        test_scores_split.append(acc_test)
        print(f"Split: {s:<3} | Train Acc: {acc_train:.4f} | Test Acc: {acc_test:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(
        depths,
        train_scores_depth,
        color="green",
        label="Train",
        marker="",
        linestyle="-",
    )
    plt.plot(depths, test_scores_depth, label="Test", marker="", linewidth=2)
    plt.axhline(
        y=acc_lr, color="purple", linestyle="-", label=f"Logistic Reg.: {acc_lr:.3f}"
    )

    plt.title("Wpływ głębokości")
    plt.xlabel("max depth")
    plt.ylabel("Accuracy")
    plt.xticks(depths)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("wykres_max_depth.png")
    plt.close()
    plt.figure(figsize=(10, 6))
    splits_str = [str(s) for s in splits]

    plt.plot(
        splits_str,
        train_scores_split,
        color="green",
        label="Train",
        marker="",
        linestyle="-",
    )
    plt.plot(splits_str, test_scores_split, label="Test", marker="", linewidth=2)
    plt.axhline(
        y=acc_lr, color="purple", linestyle="-", label=f"Logistic Reg.: {acc_lr:.3f}"
    )
    plt.title(f"Wpływ min_samples_split (dla depth={best_depth})")
    plt.xlabel("Minimalna liczba próbek do podziału")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("wykres_min_samples_split.png")
    plt.close()


if __name__ == "__main__":
    run_experiment()
