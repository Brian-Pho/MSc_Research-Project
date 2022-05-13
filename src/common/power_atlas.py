import matplotlib.patches as mpatches
from nilearn import plotting, image, datasets
from nilearn.input_data import NiftiSpheresMasker
from nilearn.connectome import ConnectivityMeasure
import numpy as np
import pandas as pd

from common.paths import POWER

POWER_NUM_NODES = 264
POWER_DATASET = datasets.fetch_coords_power_2011()
POWER_COORDS = np.vstack((POWER_DATASET.rois['x'], POWER_DATASET.rois['y'], POWER_DATASET.rois['z'])).T
POWER_LABELS = pd.read_csv(POWER, index_col='ROI')
POWER_NODE_COLORS = POWER_LABELS['Color'].values.tolist()
POWER_NETWORKS = {
    'VIS': 'Visual',
    'FPN': 'Fronto-parietal Task Control',
    'DMN': 'Default mode',
    'SMH': 'Sensory/somatomotor Hand',
    'SMM': 'Sensory/somatomotor Mouth',
    'CON': 'Cingulo-opercular Task Control',
    'AUD': 'Auditory',
    'SAL': 'Salience',
    'MEM': 'Memory retrieval',
    'VAN': 'Ventral attention',
    'CBR': 'Cerebellar',
    'SUB': 'Subcortical',
    'DAN': 'Dorsal attention',
}
# The following legend has been changed from the default Power atlas legend
#  - Extrapolated uncertain ROIs using the label of the closest ROI
#  - Changed colors: Pale blue -> lightsteelblue, Black -> navy, Teal -> lime
POWER_LEGEND = {
    'Blue': POWER_NETWORKS['VIS'],
    'Yellow': POWER_NETWORKS['FPN'],
    'Red': POWER_NETWORKS['DMN'],
    'Cyan': POWER_NETWORKS['SMH'],
    'Orange': POWER_NETWORKS['SMM'],
    'Purple': POWER_NETWORKS['CON'],
    'Pink': POWER_NETWORKS['AUD'],
    'navy': POWER_NETWORKS['SAL'],
    'Gray': POWER_NETWORKS['MEM'],
    'lime': POWER_NETWORKS['VAN'],
    'lightsteelblue': POWER_NETWORKS['CBR'],
    'Brown': POWER_NETWORKS['SUB'],
    'Green': POWER_NETWORKS['DAN'],
}


def generate_power_fc_matrix(file):
    """
    Generates a Power functional connectivity matrix from a set of fMRI (nifti) images.
    
    Assumes the Pearson correlation metric.
    """
    spheres_masker = NiftiSpheresMasker(seeds=POWER_COORDS, smoothing_fwhm=6, radius=5., standardize=True)
    time_series = spheres_masker.fit_transform(file)
    
    correlation_measure = ConnectivityMeasure(kind='correlation')
    correlation_matrix = correlation_measure.fit_transform([time_series])[0]
    
    return correlation_matrix


def to_power_fc_matrix(fc_vector):
    """
    Converts a Power connectivity vector (34716 x 1) to a matrix (264 x 264).
    
    Sets the diagonal to zero and makes the matrix symmetric about the diagonal.
    """
    fc_matrix = np.zeros((POWER_NUM_NODES, POWER_NUM_NODES))
    fc_matrix[np.triu_indices_from(fc_matrix, k=1)] = fc_vector
    fc_matrix = fc_matrix + fc_matrix.T
    return fc_matrix


def to_power_fc_vector(fc_matrix):
    """
    Converts a Power connectivity matrix (264 x 264) to a vector (34716 x 1).
    
    Discards diagonal values and assumes a symmetric matrix.
    """
    return fc_matrix[np.triu_indices(POWER_NUM_NODES, k=1)]


def get_power_fc_matrix_labels(return_system=True):
    """
    Gets a matrix (264 x 264) where each element is a pair representing the endpoints of that connection.
    
    The pair can either be ROI-to-ROI (1, 2) or Sytem-to-System ('Cerebellar', 'Cerebellar').
    """
    labels = POWER_LABELS['System'].values if return_system else POWER_LABELS.index
    
    label_matrix = []
    
    for row_label in labels:
        label_matrix.append([(row_label, col_label) for col_label in labels])
    
    return np.array(label_matrix)


def get_power_fc_vector_labels(return_system=True):
    """
    Gets a vector (34716 x 1) where each element is a pair representing the endpoints of that connection.
    """
    power_fc_matrix_labels = get_power_fc_matrix_labels(return_system)
    power_fc_vector_labels = to_power_fc_vector(power_fc_matrix_labels)
    
    return power_fc_vector_labels


def get_power_mpl_legend():
    """
    Gets the Power legend as a list of Matplotlib legend patches mapping color to system/network.
    """
    power_legend_patches = []
    
    for color, system in POWER_LEGEND.items():
        power_legend_patches.append(mpatches.Patch(color=color, label=system))
    
    return power_legend_patches
