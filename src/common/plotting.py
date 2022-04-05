import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nilearn import plotting, datasets

from common.paths import POWER

power = datasets.fetch_coords_power_2011()
coords = np.vstack((power.rois['x'], power.rois['y'], power.rois['z'])).T
power_labels = pd.read_csv(POWER, index_col='ROI')
node_colors = power_labels['Color'].values.tolist()


def plot_connections(connections, vmin=None, vmax=None, pos_neg=False, threshold="99.7%"):
    """
    Plot functional connectivity connections in multiple ways (E.g. Matrix and glass-brain/graph).
    """
    fc = create_power_fc_matrix(connections)

    plot_fc_matrix(fc, vmin, vmax)
    plot_fc_graph(fc, vmin, vmax, threshold=threshold)

    if pos_neg:
        positive_edges = np.clip(fc, 0, np.max(fc))
        positive_node_strength = convert_fc_to_node_strength(positive_edges)
        plot_fc_graph(positive_edges, 0, vmax, "YlOrRd", threshold=threshold)
        plot_node_strengths(positive_node_strength, 0, "YlOrRd")

        negative_edges = np.clip(fc, np.min(fc), 0)
        negative_node_strength = convert_fc_to_node_strength(negative_edges)
        plot_fc_graph(-negative_edges, 0, vmax, "PuBu", threshold=threshold)
        plot_node_strengths(negative_node_strength, 0, "PuBu")

#     node_strength = convert_fc_to_node_strength(fc)
#     plot_node_strengths(node_strength, 0, "Greens")
#     plot_node_strengths(node_strength, 0.5, "Greens")


def plot_fc_matrix(fc, vmin=None, vmax=None, cmap='bwr', title=None):
    """
    Plot functional connectivity matrix where the x and y axis represent nodes, and
    the cell value represents the correlation strength.
    """
    plotting.plot_matrix(fc, vmin=vmin, vmax=vmax, colorbar=True, cmap=cmap, title=title)


def plot_fc_graph(fc, emin=None, emax=None, cmap='bwr', threshold="99.7%"):
    """
    Plot functional connectivity graph where nodes in a brain are connected by edges 
    of varying strength.
    """
    plotting.plot_connectome(fc, coords, node_size=5, colorbar=True, node_color=node_colors,
                             edge_vmin=emin, edge_vmax=emax, edge_cmap=cmap, edge_threshold=threshold)


def plot_node_strengths(node_strength, threshold=None, cmap="Greens"):
    """
    Plot node strengths where each node is colored darker based on the absolute sum of
    edge weights connected to that node.
    """
    plotting.plot_markers(node_strength, coords, node_threshold=threshold,
                          node_vmin=0, node_vmax=1, node_cmap=cmap)


def create_power_fc_matrix(connections):
    """
    Create a Power et al. functional connectivity matrix of 264 x 264 ROIs.
    
    Sets the diagonal to zero and makes the matrix symmetric about the diagonal.
    """
    fc = np.zeros((264, 264))
    fc[np.triu_indices_from(fc, k=1)] = connections
    fc = fc + fc.T
    return fc


def convert_fc_to_node_strength(fc):
    """
    Convert all edges connected to a node to a node strength representing the
    absolute sum of all edges connected to that node.
    """
    node_strength = np.sum(np.abs(fc), axis=0)
    node_strength /= np.max(node_strength)
    return node_strength
