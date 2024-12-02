Flask Application for Particle Swarm Optimization (PSO)
Overview
This application provides a web-based interface for configuring and running the Particle Swarm Optimization (PSO) algorithm. It supports predefined and custom objective functions, allows input via form or file upload, and generates optimization results, visualizations, and downloadable outputs.

Features
PSO Algorithm: Optimize objective functions using PSO with configurable parameters.
Objective Functions: Choose from predefined functions or define custom ones.
File Input Support: Upload a file to specify PSO parameters and custom functions.
Visualizations: Generate 3D plots and animated GIFs of the optimization process.
Downloadable Outputs: Download the best particle's details as a text file.


Installation:
Install Dependencies: Ensure you have Python installed. Then, install required libraries:
pip install -r requirements.txt

Run the Application: Start the Flask server:
python shell.py

Usage
Web Interface
Open your web browser and navigate to http://127.0.0.1:5000/.

Use the form to specify:

Bounds: The search space for optimization (e.g., -10,10).
Number of Particles: Size of the particle swarm.
Max Iterations: Maximum number of optimization steps.
Inertia, Cognitive, and Social Coefficients: PSO parameters.
Objective Function: Choose a predefined or custom function.
Optionally, upload a file containing parameters and a custom function.

Submit the form to run the optimization and view results.

API Endpoints
/run_pso (POST): Run the PSO algorithm.

Inputs:
Form fields or file upload for PSO parameters.
Outputs:
JSON containing paths to the generated 3D plot, animation, and results file.
/download_best_particle_file (GET): Download the best particle's position as a text file.

File Format for Upload
When uploading a file, it should be structured as:


bounds: -10,10
num_particles: 30
max_iterations: 50
inertia: 0.6
cognitive: 0.5
social: 2.0
is_maximization: False
function:
math.sin(x) + math.cos(y)


Visualizations
3D Plot: Displays the objective function over the search space.
Animation: Shows the particle swarm's progress over iterations.
Generated files are returned as URLs in the API response.

Dependencies
Flask: Web framework for the application.
Matplotlib: For generating plots and animations.
Math: To handle complex mathematical evaluations.
Numpy:
base64  # Library for encoding data into base64 format
tempfile  # Module for creating temporary files
os
matplotlib.pyplot
Custom Modules: Includes modules for PSO, file handling, and visualization.


Notes
Ensure the matplotlib library is configured to use the Agg backend for server-side rendering.
For custom functions, ensure mathematical expressions are valid Python code.
Number of plot points(how detailed the plot will be) can be changed in code just rewrite NUM_POINTS = 100 to diferend positive integer, but large number of points takes significantly longer to plot
