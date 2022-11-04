"""
Holds the functions for plotting the brain data.
"""
import numpy as np
from mne.viz import circular_layout
from mne_connectivity.viz import plot_connectivity_circle
from nilearn import plotting

from common.power_atlas import (
    POWER_COORDS, POWER_LEGEND, POWER_NODE_COLORS, to_power_fc_matrix)

DEFAULT_CMAP = 'bwr'
POS_CMAP = 'YlOrRd'
NEG_CMAP = 'PuBu'


def plot_connections(
        connections, vmin=None, vmax=None, threshold="99.7%", show_matrix=False,
        show_pos_neg=True, show_node_strength=False, title=None):
    """
    Plots a functional connectivity matrix onto multiple plots.

    Plots include glass brain and matrix.

    Parameters
    ----------
    connections : np.array
    vmin : float
    vmax : float
    threshold : str
    show_matrix : bool
    show_pos_neg : bool
    show_node_strength : bool
    title : str

    Returns
    -------
    None

    """
    fc_matrix = to_power_fc_matrix(connections)

    if show_matrix:
        plot_fc_matrix(fc_matrix, vmin, vmax)
    plot_fc_graph(fc_matrix, vmin, vmax, threshold=threshold, title=title)

    if show_pos_neg:
        positive_edges = get_positive_connections(fc_matrix)
        positive_node_strength = convert_fc_to_node_strength(positive_edges)
        plot_fc_graph(positive_edges, 0, vmax, POS_CMAP, threshold=threshold)
        plot_node_strengths(positive_node_strength, 0, POS_CMAP)

        negative_edges = get_negative_connections(fc_matrix)
        negative_node_strength = convert_fc_to_node_strength(negative_edges)
        plot_fc_graph(-negative_edges, 0, vmax, NEG_CMAP, threshold=threshold)
        plot_node_strengths(negative_node_strength, 0, NEG_CMAP)

    if show_node_strength:
        node_strength = convert_fc_to_node_strength(fc_matrix)
        plot_node_strengths(node_strength, 0, "Greens")
        plot_node_strengths(node_strength, 0.5, "Greens")


def plot_fc_matrix(fc, vmin=None, vmax=None, cmap=DEFAULT_CMAP, title=None):
    """
    Plots a functional connectivity matrix where the x-axis and y-axis represent
    nodes, and the cell value represents the correlation strength.

    Parameters
    ----------
    fc : np.array
    vmin : float
    vmax : float
    cmap : str
    title : str

    Returns
    -------
    None

    """
    plotting.plot_matrix(
        fc, vmin=vmin, vmax=vmax, colorbar=True, cmap=cmap, title=title)


def plot_fc_graph(
        fc, emin=None, emax=None, cmap=DEFAULT_CMAP, threshold="99.7%",
        title=None):
    """
    Plots a functional connectivity glass brain graph where nodes in a brain
    are connected by edges of varying strength.

    Parameters
    ----------
    fc : np.array
    emin : float
    emax : float
    cmap : str
    threshold : str
    title : str

    Returns
    -------
    None

    """
    plotting.plot_connectome(
        fc, POWER_COORDS, node_size=5, colorbar=True,
        node_color=POWER_NODE_COLORS, edge_vmin=emin, edge_vmax=emax,
        edge_cmap=cmap, edge_threshold=threshold, title=title)


def plot_node_strengths(node_strength, threshold=None, cmap=DEFAULT_CMAP):
    """
    Plots a functional connectivity glass brain graph where nodes are colored
    based on the absolute sum of edge weights connected to that node.

    Parameters
    ----------
    node_strength : np.array
    threshold : str
    cmap : str

    Returns
    -------
    None

    """
    plotting.plot_markers(node_strength, POWER_COORDS, node_threshold=threshold,
                          node_vmin=0, node_vmax=1, node_cmap=cmap)


def plot_circular_graph(
        fc, title=None, sign='pos', vmin=None, vmax=None, fig=None):
    """
    Plots a circular graph where the circle is divided into arcs where each
    arc represents one Power network.

    Parameters
    ----------
    fc : np.array
    title : str
    sign : str
    vmin : float
    vmax : float
    fig : matplotlib.figure

    Returns
    -------
    connectivity circle instance

    """
    cm_sign = 'Reds' if sign == 'pos' else 'Blues'
    node_names = POWER_LEGEND.values()
    node_colors = POWER_LEGEND.keys()
    node_order = list(node_names)
    node_angles = circular_layout(node_names, node_order)

    return plot_connectivity_circle(
        fc, node_names, node_angles=node_angles,
        colormap=cm_sign, show=True, node_colors=node_colors, facecolor='white',
        textcolor='black', node_edgecolor='white', colorbar=True, fig=fig,
        title=title, vmin=vmin, vmax=vmax
    )


def convert_fc_to_node_strength(fc):
    """
    Converts all edges connected to a node to a node strength representing the
    absolute sum of all edges connected to that node.

    Parameters
    ----------
    fc : np.array

    Returns
    -------
    node_strength : np.array

    """
    node_strength = np.sum(np.abs(fc), axis=0)
    node_strength /= np.max(node_strength)
    return node_strength


def get_positive_connections(fc_matrix):
    """
    Gets only positive connections from the functional connectivity matrix.

    Parameters
    ----------
    fc_matrix : np.array

    Returns
    -------
    positive_connections : np.array

    """
    positive_connections = np.clip(fc_matrix, 0, np.max(fc_matrix))
    return positive_connections


def get_negative_connections(fc_matrix):
    """
    Gets only negative connections from the functional connectivity matrix.

    Parameters
    ----------
    fc_matrix : np.array

    Returns
    -------
    negative_connections : np.array

    """
    negative_connections = np.clip(fc_matrix, np.min(fc_matrix), 0)
    return negative_connections


def get_matrix_mask(fc_matrix_shape, part='upper'):
    """
    Gets a mask for the upper/lower triangle of a matrix.

    The mask is used to hide duplicate data since the matrix is symmetric about
    the diagonal.

    Parameters
    ----------
    fc_matrix_shape : tuple
    part : str

    Returns
    -------
    mask : np.array

    """
    mask = np.zeros(fc_matrix_shape)

    if part == 'upper':
        mask[np.triu_indices_from(mask, k=1)] = True
    elif part == 'lower':
        mask[np.tril_indices_from(mask, k=1)] = True

    return mask
    