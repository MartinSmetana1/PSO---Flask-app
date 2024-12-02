import numpy as np  # Library for numerical computations
import matplotlib.pyplot as plt  # Library for creating visualizations
import io  # Library for in-memory file handling
import base64  # Library for encoding data into base64 format
import matplotlib  # Library for creating static, animated, and interactive plots
matplotlib.use('Agg')  # Use Agg backend for non-GUI rendering (suitable for server environments)

def create_3d_graph(objective_function, bounds, NUM_POINTS):
    """
    Generate a 3D surface plot of the objective function within specified bounds.

    Args:
        objective_function (callable): The function to be plotted.
        bounds (list of tuples): The bounds of the search space [(x_min, x_max), (y_min, y_max)].
        NUM_POINTS (int): The number of points to generate in each dimension for the plot.

    Returns:
        str: A base64-encoded string representing the 3D plot in PNG format.
    """
    # Generate a grid of x and y values within the specified bounds
    x_vals = np.linspace(bounds[0][0], bounds[0][1], NUM_POINTS)  # x range
    y_vals = np.linspace(bounds[1][0], bounds[1][1], NUM_POINTS)  # y range
    X, Y = np.meshgrid(x_vals, y_vals)  # Create a 2D grid from x and y

    # Evaluate the objective function at each grid point
    Z = np.array([
        objective_function([x, y])  # Calculate function value at (x, y)
        for x, y in zip(np.ravel(X), np.ravel(Y))
    ]).reshape(X.shape)

    # Create a figure and 3D axis for plotting
    fig = plt.figure(figsize=(8, 6))  # Define figure size
    ax = fig.add_subplot(111, projection='3d')  # Add a 3D subplot

    # Plot the surface of the objective function
    ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.6)  # Use 'plasma' colormap with transparency
    ax.set_xlabel('X')  # Label for the x-axis
    ax.set_ylabel('Y')  # Label for the y-axis
    ax.set_zlabel('Objective Value')  # Label for the z-axis
    ax.set_title('Objective Function Surface')  # Title of the plot

    # Save the plot to a buffer in PNG format
    buf = io.BytesIO()  # Create an in-memory bytes buffer
    plt.savefig(buf, format="png")  # Save the plot to the buffer
    buf.seek(0)  # Reset buffer position to the beginning

    # Convert the image to a base64-encoded string
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    # Close the plot to release resources
    plt.close(fig)

    # Return the base64-encoded string
    return img_str
