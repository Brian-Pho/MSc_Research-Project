import numpy as np

from scipy import stats
from sklearn.base import clone
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RepeatedKFold
from common.calculation import calc_pvalue

N_PERM = 3000
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
    
    G_scores, G_scores_perm = _custom_permutation_test_score(
        clone(estimator), G_0[0], G_0[1], G_1[0], G_1[1], G_2[0], G_2[1], cv_0, cv_1, cv_2, n_permutations, scorer)
    
    G_mean_scores, G_pvalues = [], []
    total_permutations = n_permutations
    #     total_permutations = n_permutations * len(cv_0)

    for scores, scores_perm in zip(G_scores, G_scores_perm):
        mean_score = np.mean(scores)
        G_mean_scores.append(mean_score)
        
        scores_perm = np.array(scores_perm)
        pvalue = calc_pvalue(scores_perm, mean_score, total_permutations)
        G_pvalues.append(pvalue)

    return G_mean_scores, G_pvalues


def _custom_permutation_test_score(estimator, X_0, y_0, X_1, y_1, X_2, y_2, cv_0, cv_1, cv_2, n_permutations, scorer):
    # Index = group
    G_scores = [[], [], []]
    G_scores_perm = [[], [], []]
    
    for curr_cv in range(len(cv_0)):
        # Train and test on the in-group data
        cv_0_train, cv_0_test = cv_0[curr_cv][0], cv_0[curr_cv][1]
        X_0_train, X_0_test = X_0[cv_0_train], X_0[cv_0_test]
        y_0_train, y_0_test = y_0[cv_0_train], y_0[cv_0_test]
        
        estimator.fit(X_0_train, y_0_train)
        G_scores[0].append(scorer(estimator, X_0_test, y_0_test))
        
        # Test on the out-group data
        cv_1_test, cv_2_test = cv_1[curr_cv][1], cv_2[curr_cv][1]
        X_1_test, y_1_test = X_1[cv_1_test], y_1[cv_1_test]
        X_2_test, y_2_test = X_2[cv_2_test], y_2[cv_2_test]
        
        G_scores[1].append(scorer(estimator, X_1_test, y_1_test))
        G_scores[2].append(scorer(estimator, X_2_test, y_2_test))
        
        # Test on the shuffled out-group data
        rng = np.random.default_rng()
        G_scores_perm_temp = [[], [], []]
        X_tests = [X_0_test, X_1_test, X_2_test]
        y_tests = [y_0_test, y_1_test, y_2_test]
        
        for _ in range(n_permutations):
            for X_test, y_test, scores_temp in zip(X_tests, y_tests, G_scores_perm_temp):
#             for X_test, y_test, scores_temp in zip(X_tests, y_tests, G_scores_perm):
                y_test_perm = rng.permutation(y_test)
                scores_temp.append(scorer(estimator, X_test, y_test_perm))
        
        for score_perm, score_temp in zip(G_scores_perm, G_scores_perm_temp):
            score_perm.append(np.mean(score_temp))
        
    return G_scores, G_scores_perm
