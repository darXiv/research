"""
Publication-Quality 3D Figure: Attentional Trajectories Through Constraint Surface
WIREFRAME LANDSCAPE AESTHETIC

Inspired by classic topological visualizations with complex probability landscapes.

DESIGN PRINCIPLE:
- High-resolution wireframe mesh showing complex topography (valleys, peaks, ridges)
- X-axis: Time (0:00 to 3:00) - STRICTLY MONOTONIC
- Y-axis: Experiential Dimension 1
- Z-axis: Probability/Elevation (constraint surface height)
- 5 bright trajectories flowing through the landscape
- Green wireframe on pure black background
- Dense mesh for detailed topography
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import uniform_filter1d

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
    'savefig.pad_inches': 0.1,
    'figure.facecolor': '#000000',
    'axes.facecolor': '#000000',
})

# ============================================================================
# COLOR PALETTE
# ============================================================================

WIREFRAME_COLOR = '#7FFF00'  # Bright chartreuse green (Matrix-style)
WIREFRAME_EDGE_COLOR = '#556B2F'  # Darker olive for depth

TRAJECTORY_COLORS = [
    '#9ACD32',  # Yellow-green
    '#7FFF00',  # Chartreuse (bright - matches wireframe)
    '#6B8E23',  # Olive drab
    '#90EE90',  # Light green
    '#556B2F',  # Dark olive green
]

# ============================================================================
# COMPLEX CONSTRAINT SURFACE: Rich topography with valleys and peaks
# ============================================================================

def constraint_surface(t, y):
    """
    Create a complex probability landscape with multiple attractors (valleys)
    and repellors (peaks).

    This creates the kind of rich, wavy topography seen in the reference image.

    Parameters:
    -----------
    t : ndarray
        Time dimension (0 to 180 seconds)
    y : ndarray
        Experiential dimension 1 (0 to 2)

    Returns:
    --------
    z : ndarray
        Surface elevation (probability landscape)
    """
    # Normalize to smaller ranges for better wave behavior
    t_norm = t / 30.0  # Scale down time
    y_norm = y * 2.0   # Scale up y dimension

    # Multiple overlapping sinusoidal components create complex topology
    z = (
        # Large-scale undulations
        0.5 * np.sin(t_norm * 0.8) * np.cos(y_norm * 0.6) +

        # Medium-scale waves
        0.3 * np.cos(t_norm * 1.5 + y_norm * 1.2) +

        # Fine-grain texture
        0.2 * np.sin(t_norm * 3.0 - y_norm * 2.0) +

        # Cross-interaction terms (create ridges and valleys)
        0.25 * np.sin(t_norm * 2.0) * np.sin(y_norm * 1.5) +

        # Radial component (creates central attraction)
        -0.15 * ((t_norm - 3.0)**2 + (y_norm - 2.0)**2) * 0.05
    )

    return z

# ============================================================================
# TRAJECTORY GENERATION: Paths through the landscape
# ============================================================================

def generate_trajectory_through_landscape(trajectory_id, num_points=200):
    """
    Generate trajectories that follow the constraint surface topology.

    Trajectories are attracted to valleys and repelled by peaks, creating
    natural-looking paths through the probability landscape.

    Parameters:
    -----------
    trajectory_id : int
        Index 0-4 for different trajectories
    num_points : int
        Number of points along trajectory

    Returns:
    --------
    t, y, z : ndarray
        Trajectory coordinates
    """
    # Time axis: strictly monotonic
    t = np.linspace(0, 180, num_points)

    # Start each trajectory at slightly different Y position
    y_start = 1.0 + (trajectory_id - 2) * 0.2

    # Y dimension follows gentle oscillation with individual phase
    base_freq = 0.015
    phase = trajectory_id * 0.8
    amplitude = 0.4

    y = y_start + amplitude * np.sin(base_freq * t + phase)

    # Add drift to spread trajectories
    drift = (trajectory_id - 2) * 0.1 * (t / 180.0)
    y += drift

    # Clamp to valid range
    y = np.clip(y, 0.2, 1.8)

    # Smooth
    y = uniform_filter1d(y, size=10)

    # Z follows the surface, but elevated slightly above it
    z = constraint_surface(t, y) + 0.15

    return t, y, z

# ============================================================================
# MAIN FIGURE
# ============================================================================

def create_figure():
    """
    Create the wireframe landscape visualization.
    """
    fig = plt.figure(figsize=(14, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')

    # Pure black background
    ax.set_facecolor('#000000')
    fig.patch.set_facecolor('#000000')

    # ========================================================================
    # CREATE CONSTRAINT SURFACE MESH
    # ========================================================================

    print("Creating complex constraint surface...")

    # High resolution for detailed wireframe
    resolution_t = 120
    resolution_y = 80

    t_range = np.linspace(0, 180, resolution_t)
    y_range = np.linspace(0, 2, resolution_y)

    T_mesh, Y_mesh = np.meshgrid(t_range, y_range)
    Z_mesh = constraint_surface(T_mesh, Y_mesh)

    # Plot wireframe (NO surface fill, pure wireframe)
    ax.plot_wireframe(
        T_mesh, Y_mesh, Z_mesh,
        color=WIREFRAME_COLOR,
        alpha=0.6,
        linewidth=0.3,
        rstride=2,
        cstride=2,
    )

    # Add edge wireframe with darker color for depth perception
    ax.plot_wireframe(
        T_mesh, Y_mesh, Z_mesh,
        color=WIREFRAME_EDGE_COLOR,
        alpha=0.2,
        linewidth=0.2,
        rstride=4,
        cstride=4,
    )

    # ========================================================================
    # GENERATE AND PLOT TRAJECTORIES
    # ========================================================================

    print("Generating trajectories through landscape...")

    for i in range(5):
        t, y, z = generate_trajectory_through_landscape(i, num_points=200)

        # Plot trajectory line (thick and bright)
        ax.plot(
            t, y, z,
            color=TRAJECTORY_COLORS[i],
            linewidth=2.5,
            alpha=0.95,
            solid_capstyle='round',
            zorder=100,
        )

        # Start point marker (white)
        ax.scatter(
            [t[0]], [y[0]], [z[0]],
            color='white',
            s=40,
            alpha=1,
            zorder=150,
        )

        # End point marker
        ax.scatter(
            [t[-1]], [y[-1]], [z[-1]],
            color=TRAJECTORY_COLORS[i],
            s=50,
            alpha=1,
            zorder=150,
        )

    # ========================================================================
    # CAMERA AND AXES
    # ========================================================================

    # Viewing angle similar to reference image
    ax.view_init(elev=35, azim=-65)

    # Set limits
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 2)
    ax.set_zlim(-1.5, 1.5)

    # Hide axes for clean look (like reference image)
    ax.set_axis_off()
    ax.grid(False)

    # Remove panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')

    plt.tight_layout()

    return fig, ax

# ============================================================================
# EXPORT
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Creating wireframe landscape visualization...")
    print("=" * 70)

    fig, ax = create_figure()

    print("\nSaving figures...")
    plt.savefig('constraint_surface_wireframe.png', format='png', dpi=300, facecolor='#000000')
    plt.savefig('constraint_surface_wireframe.svg', format='svg', dpi=300, facecolor='#000000')
    plt.savefig('constraint_surface_wireframe.pdf', format='pdf', dpi=300, facecolor='#000000')

    print("\n" + "=" * 70)
    print("✓ Wireframe landscape figure generated successfully!")
    print("=" * 70)
    print("\nFiles created:")
    print("  • constraint_surface_wireframe.png")
    print("  • constraint_surface_wireframe.svg")
    print("  • constraint_surface_wireframe.pdf")
    print("\nDesign features:")
    print("  • High-resolution green wireframe mesh")
    print("  • Complex topography (valleys = attractors, peaks = repellors)")
    print("  • 5 bright trajectories flowing through landscape")
    print("  • Pure black background")
    print("  • Time axis strictly monotonic (0:00 to 3:00)")
    print("  • Matrix-inspired green/chartreuse aesthetic")
    print("=" * 70)

    plt.show()
