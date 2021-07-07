import numpy as np


def get_k_argmax(a, k):
    k_argmax = np.argpartition(a, -k)[-k:]

    return k_argmax


def multiply(v1, v2):
    return v1 * v2


def normalize_vector(v):
    return v / np.linalg.norm(v)


def calc_cosine_similarity(v1, v2):
    v1_u = normalize_vector(v1)
    v2_u = normalize_vector(v2)
    
    return np.dot(v1_u, v2_u)


def calc_norm_euclidean(v1, v2):
    v1_u = normalize_vector(v1)
    v2_u = normalize_vector(v2)
    
    return np.linalg.norm(v1_u - v2_u)


def compare_age_similarity(all_ages, bin_1, bin_2, bin_3, similarity_func):
    comparisons = []
    comparisons.append(similarity_func(all_ages, bin_1))
    comparisons.append(similarity_func(all_ages, bin_2))
    comparisons.append(similarity_func(all_ages, bin_3))
    comparisons.append(similarity_func(bin_1, bin_2))
    comparisons.append(similarity_func(bin_1, bin_3))
    comparisons.append(similarity_func(bin_2, bin_3))
    
    if similarity_func == multiply:
        return comparisons
    
    matrix = np.zeros((4, 4))
    matrix[np.triu_indices_from(matrix, k=1)] = comparisons
    matrix = matrix + matrix.T
    return matrix
