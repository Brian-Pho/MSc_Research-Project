import numpy as np


def bin_by_age(X, y, ages):
    X_bin_1, y_bin_1 = _select_data(X, y, np.where(ages <= 9))
    X_bin_2, y_bin_2 = _select_data(X, y, np.where(
        np.logical_and(ages <= 12, ages > 9)))
    X_bin_3, y_bin_3 = _select_data(X, y, np.where(ages > 12))

    return [[X_bin_1, y_bin_1], [X_bin_2, y_bin_2], [X_bin_3, y_bin_3]]


def bin_by_feature(X, y, feature, other_feature, num_bins=3):
    # Create the bins
    indices = np.arange(feature.shape[0])
    bin_indices = np.split(indices, num_bins)
    
    # Sort the data based on the feature
    sort_indices = np.argsort(feature)
    X, y = _select_data(X, y, sort_indices)
    
    # Apply the bins to the sorted data
    bins = [_select_data(X, y, bin_index) for bin_index in bin_indices]
    
    # Print bin statistics (age, sex, y)
    all_stats = [other_feature]
    for stat in all_stats:
        sorted_stat = stat[sort_indices]
        binned_stat = [sorted_stat[bin_index] for bin_index in bin_indices]
        
        for bin_num, feature_bin in enumerate(binned_stat):
#             print(f'Bin {bin_num} Range: {np.min(feature_bin):.2f} -> {np.max(feature_bin):.2f}')
            print(f'Bin {bin_num}: {np.unique(feature_bin, return_counts=True)}')
            
        print('---')
        
    return bins


def _select_data(X, y, indices):
    return X[indices], y[indices]
