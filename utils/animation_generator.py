import numpy as np  # Library for numerical operations
import matplotlib.pyplot as plt  # Library for plotting
from matplotlib import animation  # Module for creating animations
import base64  # Library for encoding data into base64 format
import tempfile  # Module for creating temporary files
import os  # Module for interacting with the operating system
import matplotlib  # Library for creating static, animated, and interactive plots
matplotlib.use('Agg')  # Use Agg backend for non-GUI rendering (suitable for servers)



def create_animation(pso,NUM_POINTS):
    """
    Create an animated contour plot visualizing the movement of particles during PSO optimization.

    Args:
        pso: A PSO (Particle Swarm Optimization) instance containing optimization data and history.

    Returns:
        A base64-encoded string of the generated animation in GIF format.
    """
    # Generate a grid of x and y values within the bounds
    x_vals = np.linspace(pso.bounds[0][0], pso.bounds[0][1], NUM_POINTS)
    y_vals = np.linspace(pso.bounds[1][0], pso.bounds[1][1], NUM_POINTS)
    X, Y = np.meshgrid(x_vals, y_vals)  # Create a 2D grid from x and y
    Z = np.array([
        pso.objective_function([x, y])  # Evaluate the objective function for each grid point
        for x, y in zip(np.ravel(X), np.ravel(Y))
    ]).reshape(X.shape)

    # Create a figure and axis for plotting
    fig, ax = plt.subplots(figsize=(8, 6))
    # Draw a contour plot of the objective function
    contour = ax.contourf(X, Y, Z, levels=50, cmap='plasma')
    ax.set_title('Objective Function Contour Plot')  # Set the title
    ax.set_xlabel('X')  # Label the x-axis
    ax.set_ylabel('Y')  # Label the y-axis

    # Scatter plot for particles and the global best marker
    scatter = ax.scatter([], [], color='red', s=50, label='Particles')  # Red dots for particles
    global_best_marker = ax.scatter([], [], color='green', s=100, label='Global Best', marker='x')  # Green 'x' for global best

    def update(frame):
        """
        Update the positions of particles and the global best for the given frame.
        
        Args:
            frame: Current frame index.

        Returns:
            Updated scatter and global_best_marker artists for animation.
        """
        # Get particle positions for the current frame
        particle_positions = pso.history[frame]
        scatter.set_offsets(particle_positions)  # Update particle positions
        # Get the global best position for the current frame
        global_best_position = pso.best_positions_per_iteration[frame]
        global_best_marker.set_offsets([global_best_position[:2]])  # Update global best position
        return scatter, global_best_marker

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=len(pso.history), blit=True  # Call update for each frame
    )

    # Save the animation to a temporary GIF file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
        ani.save(tmpfile.name, writer="pillow", fps=2)  # Save animation at 2 frames per second
        tmpfile_path = tmpfile.name  # Store the temporary file path

    # Read the GIF file and encode it as a base64 string
    with open(tmpfile_path, "rb") as f:
        img_str = base64.b64encode(f.read()).decode('utf-8')

    # Clean up by removing the temporary file
    os.remove(tmpfile_path)
    plt.close(fig)  # Close the plot to free resources
    return img_str  # Return the base64-encoded string of the animation
