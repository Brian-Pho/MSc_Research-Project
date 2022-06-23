import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RepeatedKFold

N_PERM = 500
SCORING = ['train_r', 'test_r', 'test_p_value', 'test_mse', 'test_r2']
RKF_10_10 = RepeatedKFold(n_splits=10, n_repeats=10)
RKF_5_5 = RepeatedKFold(n_splits=5, n_repeats=5)


def multimetric_scorer(model, X, y):
    """
    Scores the model on multiple metrics (Pearson r, MSE, r2).
    """
    y_pred = model.predict(X)
    
    if y_pred.ndim == 2:
        y_pred = np.squeeze(y_pred)
    
    r, p_value = stats.pearsonr(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    return {'r': r, 'p_value': p_value, 'mse': mse, 'r2': r2}


def unimetric_scorer(model, X, y):
    """
    Scores the model on one metric (Pearson r).
    """
    y_pred = model.predict(X)
    
    if y_pred.ndim == 2:
        y_pred = np.squeeze(y_pred)
        
    r, p_value = stats.pearsonr(y, y_pred)
    
    return r


def calc_pvalue(permutation_scores, score, n_permutations):
    """
    Calculates the empirical p-value against the null hypothesis that features and targets
    are independent.
    
    Get the number of permutation scores above the true score plus one, divided by
    the number of permutations plus one, to get the p-value.
    """
    return (np.sum(permutation_scores >= score) + 1.0) / (n_permutations + 1)
