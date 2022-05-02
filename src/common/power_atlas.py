import matplotlib.patches as mpatches
from nilearn import plotting, image, datasets
from nilearn.input_data import NiftiSpheresMasker
from nilearn.connectome import ConnectivityMeasure, sym_matrix_to_vec, vec_to_sym_matrix
import numpy as np
import pandas as pd

from .paths import POWER

POWER_DATASET = datasets.fetch_coords_power_2011()
POWER_COORDS = np.vstack((POWER_DATASET.rois['x'], POWER_DATASET.rois['y'], POWER_DATASET.rois['z'])).T
POWER_LABELS = pd.read_csv(POWER, index_col='ROI')
POWER_NUM_NODES = 264
# The following legend has been customized from the default legend
#  - Extrapolated uncertain ROIs using the label of the closest ROI
#  - Changed colors: Pale blue -> lightsteelblue, Black -> navy, Teal -> lime
POWER_LEGEND = {
    'Blue': 'Visual',
    'Yellow': 'Fronto-parietal Task Control',
    'Red': 'Default mode',
    'Cyan': 'Sensory/somatomotor Hand',
    'Orange': 'Sensory/somatomotor Mouth',
    'Purple': 'Cingulo-opercular Task Control',
    'Pink': 'Auditory',
    'navy': 'Salience',
    'Gray': 'Memory retrieval',
    'lime': 'Ventral attention',
    'lightsteelblue': 'Cerebellar',
    'Brown': 'Subcortical',
    'Green': 'Dorsal attention',
}


def generate_power_fc_matrix(file):
    spheres_masker = NiftiSpheresMasker(seeds=POWER_COORDS, smoothing_fwhm=6, radius=5., standardize=True)
    time_series = spheres_masker.fit_transform(file)
    
    correlation_measure = ConnectivityMeasure(kind='correlation')
    correlation_matrix = correlation_measure.fit_transform([time_series])[0]
    
    return correlation_matrix


def to_power_fc_matrix(fc_vector, labels=False):
    """
    Converts a Power connectivity vector (34716 x 1) to a matrix (264 x 264).
    
    Sets the diagonal to zero and makes the matrix symmetric about the diagonal.
    """
    if labels:
        fc_matrix = np.zeros((POWER_NUM_NODES, POWER_NUM_NODES))
        fc_matrix[np.triu_indices_from(fc_matrix, k=1)] = fc_vector
        fc_matrix = fc_matrix + fc_matrix.T
        return fc_matrix
        
    return vec_to_sym_matrix(fc_vector, np.zeros(POWER_NUM_NODES))


def to_power_fc_vector(fc_matrix, labels=False):
    """
    Converts a Power connectivity matrix (264 x 264) to a vector (34716 x 1).
    
    Discards diagonal values and assumes a symmetric matrix.
    """
    if labels:
        return fc_matrix[np.triu_indices(POWER_NUM_NODES, k=1)]

    return sym_matrix_to_vec(fc_matrix, discard_diagonal=True)


def get_power_fc_matrix_labels(return_system=False):
    labels = POWER_LABELS['System'].values if return_system else POWER_LABELS.index
    
    label_matrix = []
    
    for row_label in labels:
        row_labels = []
        label_matrix.append([(row_label, col_label) for col_label in labels])
    
    return np.array(label_matrix)


def get_power_fc_vector_labels(return_system=False):
    power_fc_matrix_labels = get_power_fc_matrix_labels(return_system)
    power_fc_vector_labels = to_power_fc_vector(power_fc_matrix_labels, True)
    
    return power_fc_vector_labels


def get_power_mpl_legend():
    power_legend_patches = []
    
    for color, system in POWER_LEGEND.items():
        power_legend_patches.append(mpatches.Patch(color=color, label=system))
    
    return power_legend_patches
