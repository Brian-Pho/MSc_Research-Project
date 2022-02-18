from collections import deque


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
