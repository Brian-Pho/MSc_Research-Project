import numpy as np

BIN_LABELS = ["All", "Bin 1", "Bin 2", "Bin 3"]
ONLY_BIN_LABELS = ["Bin 1", "Bin 2", "Bin 3"]

def get_age_bins_indices(ages):
    # Locate the indices where the condition is true
    bin_1 = np.where(ages <= 9)
    bin_2 = np.where(np.logical_and(9 < ages, ages <= 12))
    bin_3 = np.where(12 < ages)
    bin_indices = [bin_1, bin_2, bin_3]
    
    return bin_indices


def bin_by_age(X, y, ages):
    bin_indices = get_age_bins_indices(ages)
    
    # Bin the data by those indices
    if y.ndim == 1:
        bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    else:
        bins = [(X[bin_index], y[bin_index, :]) for bin_index in bin_indices]

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


def bin_data(X, y, ages=None):
    if ages and ages.any():
        bins = bin_by_age(X, y, ages, y)
        bin_1, bin_2, bin_3 = bins[0], bins[1], bins[2]
        X_all = [X, bin_1[0], bin_2[0], bin_3[0]]
        y_all = [y, bin_1[1], bin_2[1], bin_3[1]]
        bin_labels = BIN_LABELS
    else:
        X_all = [X]
        y_all = [y]
        bin_labels = ["All"]
    
    return X_all, y_all, bin_labels
