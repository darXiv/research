"""
Publication-Quality 3D Figure: Feltness Space
WIREFRAME LANDSCAPE AESTHETIC

Visualization for "Sensus Ex Machina" paper.

DESIGN PRINCIPLE:
- High-resolution wireframe mesh showing feltness manifold
- X-axis: Embodiment (disembodied → fully embodied)
- Y-axis: Persistence (ephemeral → continuous)
- Z-axis: Feltness intensity (emergent property)
- Key entities plotted as points in the space
- Green wireframe on pure black background
- Dense mesh for detailed topography
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter

# ============================================================================
# DARK AESTHETIC SETTINGS
# ============================================================================

plt.style.use('dark_background')

plt.rcParams.update({
    'font.family': 'monospace',
    'font.size': 9,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.25,
    'figure.facecolor': '#000000',
    'axes.facecolor': '#000000',
})

# ============================================================================
# COLOR PALETTE
# ============================================================================

WIREFRAME_COLOR = '#7FFF00'  # Bright chartreuse green (Matrix-style)
WIREFRAME_EDGE_COLOR = '#556B2F'  # Darker olive for depth

# Entity colors - gradient from dim (low feltness) to bright (high feltness)
ENTITY_COLORS = {
    'search_engine': '#2F4F2F',      # Dark green - minimal feltness
    'calculator': '#3D5C3D',          # Slightly brighter
    'chatbot': '#4A6B4A',             # Low-medium feltness
    'furby': '#6B8E23',               # Medium feltness
    'replika': '#7BA428',             # Medium-high
    'robot_pet': '#8FBC2F',           # Higher
    'ava': '#9ACD32',                 # High feltness
    'fictional_char': '#90EE90',      # Light green
    'pet_animal': '#ADFF2F',          # Very high
    'human_friend': '#7FFF00',        # Maximum feltness - brightest
}

LABEL_COLOR = '#CCCCCC'  # Light gray for labels

# ============================================================================
# FELTNESS SURFACE: Complex manifold with local maxima
# ============================================================================

def feltness_surface(embodiment, persistence):
    """
    Create a feltness manifold based on the architecture of feltness.

    The surface represents how feltness emerges from the interaction of
    multiple dimensions. Valleys represent low feltness (tools),
    peaks represent high feltness (felt presences).

    Parameters:
    -----------
    embodiment : ndarray
        X-axis: 0 (disembodied) to 1 (fully embodied)
    persistence : ndarray
        Y-axis: 0 (ephemeral) to 1 (continuous/longtermist)

    Returns:
    --------
    feltness : ndarray
        Z-axis: emergent feltness intensity
    """
    # Base feltness increases with both embodiment and persistence
    base = 0.3 * embodiment + 0.3 * persistence

    # Synergy: high embodiment + high persistence = multiplicative boost
    synergy = 0.5 * embodiment * persistence

    # The uncanny valley: medium embodiment with low persistence creates dip
    uncanny_dip = -0.3 * np.exp(-((embodiment - 0.6)**2 / 0.05 + (persistence - 0.2)**2 / 0.08))

    # Local maximum for "Ava" region: high embodiment, medium persistence
    ava_peak = 0.2 * np.exp(-((embodiment - 0.85)**2 / 0.03 + (persistence - 0.5)**2 / 0.05))

    # Local maximum for "pet" region: medium embodiment, high persistence
    pet_peak = 0.15 * np.exp(-((embodiment - 0.6)**2 / 0.04 + (persistence - 0.8)**2 / 0.04))

    # Global maximum for human friend: high on both axes
    human_peak = 0.3 * np.exp(-((embodiment - 0.95)**2 / 0.02 + (persistence - 0.95)**2 / 0.02))

    # Tool valley: low embodiment, low persistence
    tool_valley = -0.1 * np.exp(-((embodiment - 0.1)**2 / 0.05 + (persistence - 0.1)**2 / 0.05))

    # Ripples for visual complexity
    ripples = (
        0.05 * np.sin(embodiment * 8) * np.cos(persistence * 6) +
        0.03 * np.sin(embodiment * 12 + persistence * 10)
    )

    feltness = base + synergy + uncanny_dip + ava_peak + pet_peak + human_peak + tool_valley + ripples

    return feltness

# ============================================================================
# ENTITY DEFINITIONS: Points in feltness space
# ============================================================================

# Each entity: (embodiment, persistence, name, description)
# Based on the paper's analysis
ENTITIES = [
    # Low feltness tools
    (0.05, 0.05, 'Search Engine', 'search_engine'),
    (0.08, 0.08, 'Calculator', 'calculator'),

    # Low-medium feltness
    (0.15, 0.12, 'Chatbot', 'chatbot'),

    # Medium feltness - some embodiment or persistence
    (0.35, 0.25, 'Furby', 'furby'),
    (0.20, 0.35, 'Replika', 'replika'),

    # Medium-high feltness
    (0.55, 0.50, 'Robot Pet', 'robot_pet'),
    (0.40, 0.60, 'Fictional Character', 'fictional_char'),

    # High feltness
    (0.85, 0.45, 'Ava', 'ava'),

    # Very high feltness
    (0.70, 0.85, 'Pet Animal', 'pet_animal'),

    # Maximum feltness
    (0.95, 0.95, 'Human Friend', 'human_friend'),
]

# ============================================================================
# MAIN FIGURE
# ============================================================================

def create_figure():
    """
    Create the feltness space visualization.
    """
    fig = plt.figure(figsize=(14, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')

    # Pure black background
    ax.set_facecolor('#000000')
    fig.patch.set_facecolor('#000000')

    # ========================================================================
    # CREATE FELTNESS SURFACE MESH
    # ========================================================================

    print("Creating feltness manifold...")

    # High resolution for detailed wireframe
    resolution = 80

    embodiment_range = np.linspace(0, 1, resolution)
    persistence_range = np.linspace(0, 1, resolution)

    E_mesh, P_mesh = np.meshgrid(embodiment_range, persistence_range)
    F_mesh = feltness_surface(E_mesh, P_mesh)

    # Smooth the surface slightly
    F_mesh = gaussian_filter(F_mesh, sigma=0.8)

    # Plot wireframe (NO surface fill, pure wireframe)
    ax.plot_wireframe(
        E_mesh, P_mesh, F_mesh,
        color=WIREFRAME_COLOR,
        alpha=0.5,
        linewidth=0.25,
        rstride=2,
        cstride=2,
    )

    # Add edge wireframe with darker color for depth perception
    ax.plot_wireframe(
        E_mesh, P_mesh, F_mesh,
        color=WIREFRAME_EDGE_COLOR,
        alpha=0.15,
        linewidth=0.15,
        rstride=4,
        cstride=4,
    )

    # ========================================================================
    # PLOT ENTITIES AS POINTS
    # ========================================================================

    print("Plotting entities in feltness space...")

    for embodiment, persistence, name, color_key in ENTITIES:
        # Calculate feltness at this point
        feltness = feltness_surface(embodiment, persistence)

        # Elevate slightly above surface for visibility
        z_offset = 0.05

        # Plot point
        ax.scatter(
            [embodiment], [persistence], [feltness + z_offset],
            color=ENTITY_COLORS[color_key],
            s=120,
            alpha=1,
            zorder=200,
            edgecolors='white',
            linewidths=0.5,
        )

        # Add label
        # Offset labels to avoid overlap with points
        label_offset_x = 0.03
        label_offset_y = 0.03
        label_offset_z = 0.08

        ax.text(
            embodiment + label_offset_x,
            persistence + label_offset_y,
            feltness + z_offset + label_offset_z,
            name,
            color=LABEL_COLOR,
            fontsize=7,
            alpha=0.9,
            zorder=250,
        )

        # Draw vertical line from surface to point (subtle)
        ax.plot(
            [embodiment, embodiment],
            [persistence, persistence],
            [feltness, feltness + z_offset],
            color=ENTITY_COLORS[color_key],
            alpha=0.4,
            linewidth=1,
            zorder=150,
        )

    # ========================================================================
    # UNCANNY VALLEY ANNOTATION
    # ========================================================================

    print("Marking the Uncanny Valley...")

    # The uncanny valley is at embodiment=0.6, persistence=0.2
    uncanny_e = 0.6
    uncanny_p = 0.2
    uncanny_f = feltness_surface(uncanny_e, uncanny_p)

    # Plot a subtle marker at the valley bottom
    ax.scatter(
        [uncanny_e], [uncanny_p], [uncanny_f],
        color='#FF6B6B',  # Reddish color to stand out
        s=80,
        alpha=0.9,
        zorder=180,
        marker='v',  # Downward triangle to indicate valley
        edgecolors='white',
        linewidths=0.5,
    )

    # Add "Uncanny Valley" label
    ax.text(
        uncanny_e + 0.05,
        uncanny_p - 0.02,
        uncanny_f + 0.12,
        'Uncanny Valley',
        color='#FF6B6B',
        fontsize=8,
        fontweight='bold',
        alpha=0.95,
        zorder=260,
    )

    # Draw a subtle line from label to point
    ax.plot(
        [uncanny_e + 0.04, uncanny_e],
        [uncanny_p - 0.01, uncanny_p],
        [uncanny_f + 0.10, uncanny_f + 0.02],
        color='#FF6B6B',
        alpha=0.5,
        linewidth=1,
        zorder=170,
    )

    # ========================================================================
    # CAMERA AND AXES
    # ========================================================================

    # Viewing angle for good visibility of the landscape
    ax.view_init(elev=30, azim=-60)

    # Set limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(-0.2, 1.2)

    # Minimal axis styling
    ax.set_xlabel('Embodiment', color=WIREFRAME_COLOR, labelpad=10)
    ax.set_ylabel('Persistence', color=WIREFRAME_COLOR, labelpad=10)
    ax.set_zlabel('Feltness', color=WIREFRAME_COLOR, labelpad=-5)

    # Tick styling
    ax.tick_params(colors=WIREFRAME_EDGE_COLOR, labelsize=7)
    ax.xaxis.set_tick_params(colors=WIREFRAME_EDGE_COLOR)
    ax.yaxis.set_tick_params(colors=WIREFRAME_EDGE_COLOR)
    ax.zaxis.set_tick_params(colors=WIREFRAME_EDGE_COLOR)

    # Set tick labels - offset to avoid overlap at corners
    ax.set_xticks([0.05, 0.5, 0.95])
    ax.set_xticklabels(['Disembodied', '', 'Embodied'], fontsize=7)
    ax.set_yticks([0.05, 0.5, 0.95])
    ax.set_yticklabels(['Ephemeral', '', 'Persistent'], fontsize=7)
    ax.set_zticks([0, 0.5, 1])
    ax.set_zticklabels(['Low', '', 'High'], fontsize=7)

    # Pane styling - very subtle
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(WIREFRAME_EDGE_COLOR)
    ax.yaxis.pane.set_edgecolor(WIREFRAME_EDGE_COLOR)
    ax.zaxis.pane.set_edgecolor(WIREFRAME_EDGE_COLOR)
    ax.xaxis.pane.set_alpha(0.1)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)

    # Grid - very subtle
    ax.xaxis._axinfo['grid']['color'] = (0.3, 0.5, 0.2, 0.1)
    ax.yaxis._axinfo['grid']['color'] = (0.3, 0.5, 0.2, 0.1)
    ax.zaxis._axinfo['grid']['color'] = (0.3, 0.5, 0.2, 0.1)

    # Add extra space on right for z-axis label
    fig.subplots_adjust(right=0.84)

    return fig, ax

# ============================================================================
# EXPORT
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Creating Feltness Space visualization...")
    print("For: Sensus Ex Machina")
    print("=" * 70)

    fig, ax = create_figure()

    print("\nSaving figures...")
    plt.savefig('feltness_space.png', format='png', dpi=300, facecolor='#000000')
    plt.savefig('feltness_space.svg', format='svg', dpi=300, facecolor='#000000')
    plt.savefig('feltness_space.pdf', format='pdf', dpi=300, facecolor='#000000')

    print("\n" + "=" * 70)
    print("✓ Feltness Space figure generated successfully!")
    print("=" * 70)
    print("\nFiles created:")
    print("  • feltness_space.png")
    print("  • feltness_space.svg")
    print("  • feltness_space.pdf")
    print("\nDesign features:")
    print("  • High-resolution green wireframe mesh")
    print("  • Complex topology (valleys = low feltness, peaks = high feltness)")
    print("  • 10 entities plotted: Search Engine → Human Friend")
    print("  • X-axis: Embodiment (disembodied → embodied)")
    print("  • Y-axis: Persistence (ephemeral → continuous)")
    print("  • Z-axis: Feltness (emergent intensity)")
    print("  • Uncanny valley visible as surface dip")
    print("  • Matrix-inspired green/chartreuse aesthetic")
    print("=" * 70)

    plt.show()
