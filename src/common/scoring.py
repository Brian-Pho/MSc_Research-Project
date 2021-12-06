import numpy as np

from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RepeatedKFold

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
