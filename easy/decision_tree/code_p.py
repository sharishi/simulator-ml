from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class Node:
    """
    A node in a decision tree.

    Parameters
    ----------
    feature : int, optional (default=None)
        The feature index used for splitting the node.
    threshold : float, optional (default=None)
        The threshold value at the node.
    n_samples : int, optional (default=None)
        The number of samples at the node.
    value : int, optional (default=None)
        The value of the node (i.e., the mean target value of the samples at the node).
    mse : float, optional (default=None)
        The mean squared error of the node (i.e., the impurity criterion).
    left : Node, optional (default=None)
        The left child node.
    right : Node, optional (default=None)
        The right child node.
    """

    feature: int = None
    threshold: float = None
    n_samples: int = None
    value: int = None
    mse: float = None
    left: Node = None
    right: Node = None


@dataclass
class DecisionTreeRegressor:
    """Decision tree regressor."""
    max_depth: int
    min_samples_split: int = 2

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeRegressor:
        """Build a decision tree regressor from the training set (X, y)."""
        self.n_features_ = X.shape[1]
        self.tree_ = self._split_node(X, y)
        return self

    def _mse(self, y: np.ndarray) -> float:
        """Compute the mse criterion for a given set of target values."""
        return np.mean((y - np.mean(y)) ** 2)

    def _weighted_mse(self, y_left: np.ndarray, y_right: np.ndarray) -> float:
        """Compute the weighted mse criterion for two given sets of target values."""
        if y_left.size == 0 or y_right.size == 0:
            return float('inf')
        num = self._mse(y_left) * y_left.size + self._mse(y_right) * y_right.size
        den = y_left.size + y_right.size
        return num / den

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        """Find the best split for a node."""
        node_size = y.size
        if node_size < self.min_samples_split:
            return None, None
        node_mse = self._mse(y)
        best_mse = node_mse
        best_idx, best_thr = None, None
        for idx in range(self.n_features_):
            thresholds = np.unique(X[:, idx])
            for thr in thresholds:
                left = y[X[:, idx] <= thr]
                right = y[X[:, idx] > thr]

                if left.size == 0 or right.size == 0:
                    continue

                weighted_mse = self._weighted_mse(left, right)
                if weighted_mse < best_mse:
                    best_mse = weighted_mse
                    best_idx = idx
                    best_thr = thr

        return best_idx, best_thr

    def _split_node(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """Split a node and return the resulting left and right child nodes."""
        if depth == self.max_depth or y.size < self.min_samples_split:
            return Node(value=int(round(np.mean(y))), mse=self._mse(y))

        best_idx, best_thr = self._best_split(X, y)
        if best_thr is None:
            return None

        left_idx = X[:, best_idx] <= best_thr
        right_idx = X[:, best_idx] > best_thr

        left_child = self._split_node(X[left_idx], y[left_idx], depth + 1)
        right_child = self._split_node(X[right_idx], y[right_idx], depth + 1)

        return Node(feature=best_idx, threshold=best_thr, left=left_child, right=right_child,
                    value=int(round(np.mean(y))),
                    mse=self._mse(y))
