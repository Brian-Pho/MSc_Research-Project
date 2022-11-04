"""
Holds the functions for the cross-prediction (out-of-sample cross-validation) procedure.
"""
from collections import deque

import numpy as np
from sklearn.base import clone

from common.scoring import calc_pvalue


def get_group_cv_splits(groups, cv):
    """
    Gets the group cross-validation splits.

    Used to pre-split the groups into cross-validation folds because the
    normal cross-validation function generates the folds as needed, but this
    function generates the folds all at once. Useful for cross-prediction.

    Parameters
    ----------
    groups : list
    cv : sklearn.cross_validation instance

    Returns
    -------
    groups_cv_splits : list
        A list containing all cross-validation folds.

    Notes
    -----
    Normally the train/test split is done right before training and testing,
    but this function will split the data for all cross folds before any
    training/testing is done. This is useful for keeping the training and
    testing sets consistent between cross-predictions.

    """
    groups_cv_splits = []

    for group in groups:
        group_cv = [(train, test) for train, test in cv.split(group[0])]
        groups_cv_splits.append(group_cv)

    return groups_cv_splits


def get_group_order(groups, cvs, labels):
    """
    Gets the train-test group order for cross-prediction.

    Given a list of groups, this function will return the order for train-test
    cross-prediction where the first index is always the training set.

    Parameters
    ----------
    groups : list
    cvs : list
    labels : list

    Returns
    -------
    group_order : list
    cv_order : list
    label_order : list

    Notes
    -----
    The order for 'groups', 'cvs', and 'labels' must be consistent.

    Examples
    --------
    >>> groups = [Bin 1, Bin 2, Bin 3]
    >>> cvs = [bin_1_cv, bin_2_cv, bin_3_cv]
    >>> labels = ['Bin 1', 'Bin 2', 'Bin 3']
    >>> get_group_order(groups, cvs, labels)
    ([[bin_1, bin_2, bin_3],
      [bin_2, bin_3, bin_1],
      [bin_3, bin_1, bin_2]],

    [[bin_1_cv, bin_2_cv, bin_3_cv],
     [bin_2_cv, bin_3_cv, bin_1_cv],
     [bin_3_cv, bin_1_cv, bin_2_cv]],

    [['Bin 1', 'Bin 2', 'Bin 3'],
     ['Bin 2', 'Bin 3', 'Bin 1'],
     ['Bin 3', 'Bin 1', 'Bin 2']])

    """
    groups_queue, cvs_queue, labels_queue = deque(groups), deque(cvs), deque(labels)
    group_order, cv_order, label_order = [], [], []

    for idx in range(len(groups_queue)):
        group_order.append(groups_queue.copy())
        cv_order.append(cvs_queue.copy())
        label_order.append(labels_queue.copy())

        groups_queue.rotate(-1)
        cvs_queue.rotate(-1)
        labels_queue.rotate(-1)

    return group_order, cv_order, label_order


def cross_prediction_permutation_test_score(
        estimator, group_zero, group_one, group_two, cv_zero, cv_one, cv_two,
        n_permutations=100, scorer=None):
    """
    Custom permutation test function based on:
    https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.permutation_test_score.html

    Extended to handle multiple testing sets used in cross-prediction.

    Parameters
    ----------
    estimator : sklearn.model
    group_zero : np.array
    group_one : np.array
    group_two : np.array
    cv_zero : np.array
    cv_one : np.array
    cv_two : np.array
    n_permutations : int
    scorer : sklearn.estimator

    Returns
    -------
    tuple
        First element is a list of true scores, second element is a list of
        permutation scores, third element is a list of p-values.

    """
    true_scores = _cross_prediction_permutation_test_score(
        clone(estimator), group_zero[0], group_zero[1], group_one[0],
        group_one[1], group_two[0], group_two[1], cv_zero, cv_one, cv_two,
        scorer)

    permutation_scores = []
    for _ in range(n_permutations):
        permutation_score = _cross_prediction_permutation_test_score(
            clone(estimator), group_zero[0], _shuffle(group_zero[1]),
            group_one[0], _shuffle(group_one[1]),
            group_two[0], _shuffle(group_two[1]), cv_zero, cv_one, cv_two,
            scorer)
        permutation_scores.append(permutation_score)

    permutation_scores = np.array(permutation_scores).T

    pvalues = []
    for true_score, perm_score in zip(true_scores, permutation_scores):
        pvalue = calc_pvalue(perm_score, true_score, n_permutations)
        pvalues.append(pvalue)

    return true_scores, permutation_scores, pvalues


def _cross_prediction_permutation_test_score(
        estimator, X_0, y_0, X_1, y_1, X_2, y_2, cv_0, cv_1, cv_2, scorer):
    """
    Helper function for cross_prediction_permutation_test_score() that splits
    the dataset by the given cross-validation scheme and trains and tests the
    model.

    Given three groups and their cross-fold validation splits, train on the
    first group and test on all three groups. Return the average score from
    all cross-folds.

    Parameters
    ----------
    estimator : sklearn.model
    X_0 : np.array
    y_0 : np.array
    X_1 : np.array
    y_1 : np.array
    X_2 : np.array
    y_2 : np.array
    cv_0 : np.array
    cv_1 : np.array
    cv_2 : np.array
    scorer : sklearn.scorer

    Returns
    -------
    int
        The model's average score across all cross folds.

    """
    group_scores = [[], [], []]

    for curr_cv_0, curr_cv_1, curr_cv_2 in zip(cv_0, cv_1, cv_2):
        # Train and test on the in-group data
        cv_0_train, cv_0_test = curr_cv_0[0], curr_cv_0[1]
        X_0_train, y_0_train = X_0[cv_0_train], y_0[cv_0_train]
        X_0_test, y_0_test = X_0[cv_0_test], y_0[cv_0_test]

        estimator.fit(X_0_train, y_0_train)
        group_scores[0].append(scorer(estimator, X_0_test, y_0_test))

        # Test on the out-group data
        cv_1_test, cv_2_test = curr_cv_1[1], curr_cv_2[1]
        X_1_test, y_1_test = X_1[cv_1_test], y_1[cv_1_test]
        X_2_test, y_2_test = X_2[cv_2_test], y_2[cv_2_test]

        group_scores[1].append(scorer(estimator, X_1_test, y_1_test))
        group_scores[2].append(scorer(estimator, X_2_test, y_2_test))

    # Average the scores for each group independently
    return np.mean(group_scores, axis=1)


def _shuffle(y):
    """
    Shuffles the given array.

    Helper function for cross_prediction_permutation_test_score().

    Parameters
    ----------
    y : np.array

    Returns
    -------
    np.array
        The given array randomly shuffled.

    """
    return np.random.default_rng().permutation(y)
