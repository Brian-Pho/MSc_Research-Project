import numpy as np

from scipy import stats
from sklearn.base import clone
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RepeatedKFold
from common.calculation import calc_pvalue

N_PERM = 1000
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
    
    G_0_scores, G_1_scores, G_2_scores, G_1_scores_perm, G_2_scores_perm = _custom_permutation_test_score(
        clone(estimator), G_0[0], G_0[1], G_1[0], G_1[1], G_2[0], G_2[1], cv_0, cv_1, cv_2, n_permutations, scorer)
            
    G_0_score, G_1_score, G_2_score = np.mean(G_0_scores), np.mean(G_1_scores), np.mean(G_2_scores)
    
    G_1_scores_perm, G_2_scores_perm = np.array(G_1_scores_perm), np.array(G_2_scores_perm)
        
    total_permutations = n_permutations * len(cv_0)
    
    G_1_pvalue = calc_pvalue(G_1_scores_perm, G_1_score, total_permutations)
    G_2_pvalue = calc_pvalue(G_2_scores_perm, G_2_score, total_permutations)

    return G_0_score, G_1_score, G_2_score, G_1_pvalue, G_2_pvalue


def _custom_permutation_test_score(estimator, X_0, y_0, X_1, y_1, X_2, y_2, cv_0, cv_1, cv_2, n_permutations, scorer):
    
    G_0_scores, G_1_scores, G_2_scores = [], [], []
    G_1_scores_perm, G_2_scores_perm = [], []
    
    for curr_cv in range(len(cv_0)):
        # Train and test on the in-group data
        cv_0_train, cv_0_test = cv_0[curr_cv][0], cv_0[curr_cv][1]
        X_0_train, X_0_test = X_0[cv_0_train], X_0[cv_0_test]
        y_0_train, y_0_test = y_0[cv_0_train], y_0[cv_0_test]
        
        estimator.fit(X_0_train, y_0_train)
        G_0_scores.append(scorer(estimator, X_0_test, y_0_test))
        
        # Test on the out-group data
        cv_1_test, cv_2_test = cv_1[curr_cv][1], cv_2[curr_cv][1]
        X_1_test, y_1_test = X_1[cv_1_test], y_1[cv_1_test]
        X_2_test, y_2_test = X_2[cv_2_test], y_2[cv_2_test]
        
        G_1_scores.append(scorer(estimator, X_1_test, y_1_test))
        G_2_scores.append(scorer(estimator, X_2_test, y_2_test))
        
        # Test on the shuffled out-group data
        rng = np.random.default_rng()
#         G_1_scores_perm_temp, G_2_scores_perm_temp = [], []
        for _ in range(n_permutations):
            y_1_test_perm = rng.permutation(y_1_test)
            y_2_test_perm = rng.permutation(y_2_test)
            
#             G_1_scores_perm_temp.append(scorer(estimator, X_1_test, y_1_test_perm))
#             G_2_scores_perm_temp.append(scorer(estimator, X_2_test, y_2_test_perm))
            G_1_scores_perm.append(scorer(estimator, X_1_test, y_1_test_perm))
            G_2_scores_perm.append(scorer(estimator, X_2_test, y_2_test_perm))
            
#         G_1_scores_perm.append(np.mean(G_1_scores_perm_temp))
#         G_2_scores_perm.append(np.mean(G_2_scores_perm_temp))
        
    return G_0_scores, G_1_scores, G_2_scores, G_1_scores_perm, G_2_scores_perm
