import numpy as np
from nilearn import plotting, datasets

power = datasets.fetch_coords_power_2011()
coords = np.vstack((power.rois['x'], power.rois['y'], power.rois['z'])).T


def plot_connections(connections, mi_mode=True):
    fc = create_power_fc_matrix(connections)
    cmap = 'bone' if mi_mode else 'bwr'
    plotting.plot_matrix(fc, colorbar=True, cmap=cmap)
    plotting.plot_connectome(fc, coords, edge_threshold=0, node_size=5, colorbar=True)

    node_strength = convert_fc_to_node_strength(fc)

    plotting.plot_markers(
        node_strength, coords, node_threshold=0,
        node_vmin=np.amin(connections))
    plotting.plot_markers(
        node_strength, coords, node_threshold=0.5,
        node_vmin=np.amin(connections))


def create_power_fc_matrix(connections):
    fc = np.zeros((264, 264))
    fc[np.triu_indices(264, k=1)] = connections
    fc = fc + fc.T
    return fc


def convert_fc_to_node_strength(fc):
    # calculate normalized, absolute strength for each node
    node_strength = np.sum(np.abs(fc), axis=0)
    node_strength /= np.max(node_strength)

    return node_strength
