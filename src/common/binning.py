import numpy as np

BIN_LABELS = ["All", "Bin 1", "Bin 2", "Bin 3"]
ONLY_BIN_LABELS = ["Bin 1", "Bin 2", "Bin 3"]


def get_age_bins_indices(ages):
    """
    Locate the subjects/indicies where the condition is true.
    """
    bin_1 = np.where(ages <= 9)
    bin_2 = np.where(np.logical_and(9 < ages, ages <= 12))
    bin_3 = np.where(12 < ages)
    bin_indices = [bin_1, bin_2, bin_3]
    
#     bin_1 = np.where(ages <= 10)
#     bin_2 = np.where(10 < ages)
#     bin_indices = [bin_1, bin_2]
    
    return bin_indices


def bin_by_age(X, y, ages):
    """
    Bin the dataset by age.
    
    Returns three age bins: 6-> 9, 9 -> 12, and 12 -> 16.
    """
    bin_indices = get_age_bins_indices(ages)
    
    # Bin the data by those indices
    if y.ndim == 1:
        bins = [(X[bin_index], y[bin_index]) for bin_index in bin_indices]
    else:
        bins = [(X[bin_index], y[bin_index, :]) for bin_index in bin_indices]

    return bins


def bin_data(X, y, ages=None, include_all=False):
    """
    Bin the dataset by age if ages is given.
    
    Returns either the original data or the binned data.
    """
    if ages is not None and ages.any():
        bins = bin_by_age(X, y, ages)
        bin_1, bin_2, bin_3 = bins[0], bins[1], bins[2]
        
        if include_all:
            X_bins = [X, bin_1[0], bin_2[0], bin_3[0]]
            y_bins = [y, bin_1[1], bin_2[1], bin_3[1]]
            bin_labels = BIN_LABELS
        else:
            X_bins = [bin_1[0], bin_2[0], bin_3[0]]
            y_bins = [bin_1[1], bin_2[1], bin_3[1]]
            bin_labels = ONLY_BIN_LABELS

#         bin_1, bin_2 = bins[0], bins[1]
#         X_bins = [bin_1[0], bin_2[0]]
#         y_all = [bin_1[1], bin_2[1]]
#         bin_labels = ONLY_BIN_LABELS[:2]
        
    else:
        X_bins = [X]
        y_bins = [y]
        bin_labels = ["All"]
    
    return np.array(X_bins, dtype=object), np.array(y_bins, dtype=object), np.array(bin_labels, dtype=object)
