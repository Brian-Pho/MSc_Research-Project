import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from nilearn import plotting, datasets

power = datasets.fetch_coords_power_2011()
coords = np.vstack((power.rois['x'], power.rois['y'], power.rois['z'])).T


def plot_connections(connections, vmin, vmax, mi_mode=False):
    fc = create_power_fc_matrix(connections)
    cmap = 'bone' if mi_mode else 'bwr'

    plot_fc_matrix(fc, vmin, vmax, cmap)
    plot_fc_graph(fc, vmin, vmax)

    if not mi_mode:
        positive_edges = np.clip(fc, 0, np.max(fc))
        positive_node_strength = convert_fc_to_node_strength(positive_edges)
        plot_fc_graph(positive_edges, 0, vmax, "YlOrRd")
        plot_node_strengths(positive_node_strength, 0, "YlOrRd")

        negative_edges = np.clip(fc, np.min(fc), 0)
        negative_node_strength = convert_fc_to_node_strength(negative_edges)
        plot_fc_graph(-negative_edges, 0, vmax, "PuBu")
        plot_node_strengths(negative_node_strength, 0, "PuBu")

#     node_strength = convert_fc_to_node_strength(fc)
#     plot_node_strengths(node_strength, 0, "Greens")
#     plot_node_strengths(node_strength, 0.5, "Greens")


def plot_fc_matrix(fc, vmin=None, vmax=None, cmap='bwr'):
    plotting.plot_matrix(fc, vmin=vmin, vmax=vmax, colorbar=True, cmap=cmap)


def plot_fc_graph(fc, emin=None, emax=None, cmap='bwr'):
    plotting.plot_connectome(fc, coords, node_size=5, colorbar=True,
                             edge_vmin=emin, edge_vmax=emax, edge_cmap=cmap)


def plot_node_strengths(node_strength, threshold=None, cmap="Greens"):
    plotting.plot_markers(node_strength, coords, node_threshold=threshold,
                          node_vmin=0, node_vmax=1, node_cmap=cmap)


def create_power_fc_matrix(connections):
    fc = np.zeros((264, 264))
    fc[np.triu_indices_from(fc, k=1)] = connections
    fc = fc + fc.T
    return fc


def convert_fc_to_node_strength(fc):
    # calculate normalized, absolute strength for each node
    node_strength = np.sum(np.abs(fc), axis=0)
    node_strength /= np.max(node_strength)
    return node_strength


def plot_age_comparisons(comparisons):
    f, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(comparisons, annot=True, fmt=".3f", linewidths=.5, ax=ax)