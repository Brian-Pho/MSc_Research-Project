import numpy as np

from scipy import stats
from sklearn.base import clone
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RepeatedKFold

N_PERM = 500
SCORING = ['train_r', 'test_r', 'test_p_value', 'test_mse']
RKF_10_10 = RepeatedKFold(n_splits=10, n_repeats=10)


def multimetric_scorer(model, X, y):
    y_pred = model.predict(X)
    
    if y_pred.ndim == 2:
        y_pred = np.squeeze(y_pred)
    
    r, p_value = stats.pearsonr(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    return {'r': r, 'p_value': p_value, 'mse': mse}


def unimetric_scorer(model, X, y):
    y_pred = model.predict(X)
    
    if y_pred.ndim == 2:
        y_pred = np.squeeze(y_pred)
        
    r, _ = stats.pearsonr(y, y_pred)
    
    return r


def custom_permutation_test_score(
    estimator, G_0, G_1, G_2, cv_0, cv_1, cv_2, n_permutations=100, scorer=None):
    # https://github.com/scikit-learn/scikit-learn/blob/0d378913b/sklearn/model_selection/_validation.py#L1164
    
    true_scores = _custom_permutation_test_score(
        clone(estimator), G_0[0], G_0[1], G_1[0], G_1[1], G_2[0], G_2[1], cv_0, cv_1, cv_2, scorer)
    
    permutation_scores = []
    for _ in range(n_permutations):
        permutation_scores.append(_custom_permutation_test_score(
            clone(estimator), G_0[0], _shuffle(G_0[1]), G_1[0], _shuffle(G_1[1]), 
            G_2[0], _shuffle(G_2[1]), cv_0, cv_1, cv_2, scorer))
    permutation_scores = np.array(permutation_scores).T
    
    pvalues = []
    for true_score, perm_score in zip(true_scores, permutation_scores):
        pvalues.append(calc_pvalue(perm_score, true_score, n_permutations))
    
    return true_scores, permutation_scores, pvalues


def _custom_permutation_test_score(estimator, X_0, y_0, X_1, y_1, X_2, y_2, cv_0, cv_1, cv_2, scorer):
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
    
    return np.mean(G_scores, axis=1)


def _shuffle(y):
    rng = np.random.default_rng()
    return rng.permutation(y)


def calc_pvalue(permutation_scores, score, n_permutations):
    return (np.sum(permutation_scores >= score) + 1.0) / (n_permutations + 1)