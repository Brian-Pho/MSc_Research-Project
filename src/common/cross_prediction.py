from collections import deque
from joblib import Parallel

import numpy as np
from sklearn.base import clone

from common.scoring import calc_pvalue


def get_group_cv_splits(groups, cv):
    """
    Presplit the groups using the given cross-validation scheme.
    
    Normally, the train/test split is done right before training and testing, 
    but this function will presplit the data for all cross folds before any 
    training/testing is done.
    
    This is useful for keeping the training and testing sets consistent between
    cross-predictions.
    """
    groups_cv_splits = []
    
    for group in groups:
        group_cv = [(train, test) for train, test in cv.split(group[0])]
        groups_cv_splits.append(group_cv)
    
    return groups_cv_splits


def get_group_order(groups, cvs, labels):
    """
    Compute the train-test group order for cross-prediction.
    
    Given a list of groups, this function will return the order for train-test 
    cross-prediction where the first index is always the training set.
    
    Note: The order for 'groups', 'cvs', and 'labels' must be consistent.
    
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
    g, c, l = deque(groups), deque(cvs), deque(labels)
    group_order, cv_order, label_order = [], [], []
    
    for idx in range(len(g)):     
        group_order.append(g.copy())
        cv_order.append(c.copy())
        label_order.append(l.copy())
        
        g.rotate(-1)
        c.rotate(-1)
        l.rotate(-1)
    
    return group_order, cv_order, label_order


def cross_prediction_permutation_test_score(
    estimator, G_0, G_1, G_2, cv_0, cv_1, cv_2, n_permutations=100, scorer=None):
    """
    Custom permutation test function based off of: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.permutation_test_score.html
    
    Is extended from the scikit-learn version to handle multiple testing sets 
    used in cross-prediction.
    """
    true_scores = _cross_prediction_permutation_test_score(
        clone(estimator), G_0[0], G_0[1], G_1[0], G_1[1], G_2[0], G_2[1], cv_0, cv_1, cv_2, scorer)
    
    permutation_scores = []
    for _ in range(n_permutations):
        permutation_score = _cross_prediction_permutation_test_score(
            clone(estimator), G_0[0], _shuffle(G_0[1]), G_1[0], _shuffle(G_1[1]), 
            G_2[0], _shuffle(G_2[1]), cv_0, cv_1, cv_2, scorer)
        permutation_scores.append(permutation_score)
        
    permutation_scores = np.array(permutation_scores).T
    
    pvalues = []
    for true_score, perm_score in zip(true_scores, permutation_scores):
        pvalue = calc_pvalue(perm_score, true_score, n_permutations)
        pvalues.append(pvalue)
    
    return true_scores, permutation_scores, pvalues


def _cross_prediction_permutation_test_score(estimator, X_0, y_0, X_1, y_1, X_2, y_2, cv_0, cv_1, cv_2, scorer):
    """
    Helper function for cross_prediction_permutation_test_score.
    
    Given three groups and their cross-fold validation splits, train on the first
    group, and test on all three groups. Return the average score from all cross-folds.
    """
    G_scores = [[], [], []]
        
    for curr_cv_0, curr_cv_1, curr_cv_2 in zip(cv_0, cv_1, cv_2):
        # Train and test on the in-group data
        cv_0_train, cv_0_test = curr_cv_0[0], curr_cv_0[1]
        X_0_train, y_0_train = X_0[cv_0_train], y_0[cv_0_train]
        X_0_test, y_0_test = X_0[cv_0_test], y_0[cv_0_test]
        
        estimator.fit(X_0_train, y_0_train)
        G_scores[0].append(scorer(estimator, X_0_test, y_0_test))
        
        # Test on the out-group data
        cv_1_test, cv_2_test = curr_cv_1[1], curr_cv_2[1]
        X_1_test, y_1_test = X_1[cv_1_test], y_1[cv_1_test]
        X_2_test, y_2_test = X_2[cv_2_test], y_2[cv_2_test]
        
        G_scores[1].append(scorer(estimator, X_1_test, y_1_test))
        G_scores[2].append(scorer(estimator, X_2_test, y_2_test))
    
    # Average the scores for each group independently
    return np.mean(G_scores, axis=1)


def _shuffle(y):
    """
    Helper function for cross_prediction_permutation_test_score.
    
    Shuffle the data's targets.
    """
    return np.random.default_rng().permutation(y)
