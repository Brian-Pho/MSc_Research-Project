import numpy as np


def bin_by_age(X, y, ages, other_feature, print_stats=False):
    # Locate the indices where the condition is true
    bin_1 = np.where(ages <= 9)
    bin_2 = np.where(np.logical_and(9 < ages, ages <= 12))
    bin_3 = np.where(12 < ages)
    bin_indices = [bin_1, bin_2, bin_3]
    
    # Bin the data by those indices
    if y.ndim == 1:
        bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    else:
        bins = [(X[bin_index], y[bin_index, :]) for bin_index in bin_indices]
    
    # Print out statistics (min/max age, IQ, etc.) for each bin
    if print_stats:
        all_stats = [ages, other_feature]
        for stat in all_stats:
            binned_stat = [stat[bin_index] for bin_index in bin_indices]

            for bin_num, feature_bin in enumerate(binned_stat):
                print(f'Bin {bin_num} Range: {np.min(feature_bin):.2f} -> {np.max(feature_bin):.2f}')
    #             print(f'Bin {bin_num}: {np.unique(feature_bin, return_counts=True)}')
            print('---')

    return bins


def equal_bin_by_feature(X, y, feature, other_feature, num_bins=3):
    # Create the bins
    indices = np.arange(feature.shape[0])
    bin_indices = np.split(indices, num_bins)
    
    # Sort the data based on the feature
    sort_indices = np.argsort(feature)
    X, y = _select_data(X, y, sort_indices)
    
    # Apply the bins to the sorted data
    bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    
    # Print bin statistics (age, sex, y)
    all_stats = [other_feature]
    for stat in all_stats:
        sorted_stat = stat[sort_indices]
        binned_stat = [sorted_stat[bin_index] for bin_index in bin_indices]
        
        for bin_num, feature_bin in enumerate(binned_stat):
            print(f'Bin {bin_num} Range: {np.min(feature_bin):.2f} -> {np.max(feature_bin):.2f}')
#             print(f'Bin {bin_num}: {np.unique(feature_bin, return_counts=True)}')
        print('---')
        
    return bins
