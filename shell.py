from flask import Flask, render_template, request, jsonify, send_file
from models.pso import PSO  # Import the PSO class from a separate module
from utils.objective_functions import predefined_functions  # Import predefined objective functions
from utils.file_handling import parse_file, create_text_file  # Utilities for file parsing and creation
from utils.animation_generator import create_animation  # Utility to generate animations of PSO results
from utils.image_generator import create_3d_graph  # Utility to generate 3D plots of the objective function
import math  # Import math library for complex evaluations in custom functions
import matplotlib  # Library for creating visualizations
matplotlib.use('Agg')  # Use Agg backend for non-GUI rendering (required for servers without a display)

# Initialize the Flask app
app = Flask(__name__)
NUM_POINTS = 100

@app.route('/')
def index():
    """Render the main page with a form for PSO parameter inputs."""
    return render_template('index.html', predefined_functions=predefined_functions)

@app.route('/run_pso', methods=['POST'])
def run_pso():
    """
    Handle the form submission or file upload to run PSO (Particle Swarm Optimization).
    Process inputs, configure PSO parameters, execute the optimization, and return results.
    """
    # Determine input type (form input or file upload)
    input_type = request.form.get('input_type', 'form')

    # Default PSO parameters
    params = {
        'bounds': "-10,10",  # Search space bounds
        'num_particles': 30,  # Number of particles in the swarm
        'max_iterations': 50,  # Number of iterations
        'inertia': 0.6,  # Inertia weight for velocity update
        'cognitive': 0.5,  # Cognitive (personal) learning coefficient
        'social': 2.0,  # Social (group) learning coefficient
        'is_maximization': False  # Objective is minimization by default
    }
    custom_function_code = None  # Store custom objective function code if provided
    bounds_input = params['bounds']  # Default bounds

    # Handle file upload for parameters
    if input_type == 'file':
        param_file = request.files.get('param_file')
        if param_file:
            try:
                # Parse file to extract parameters and custom function code
                params, custom_function_code = parse_file(param_file, params)
                bounds_input = params.get('bounds', bounds_input)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "File upload is required when input type is file."}), 400

    # Handle form input for parameters
    else:
        bounds_input = request.form.get('bounds', params['bounds'])
        params['num_particles'] = int(request.form.get('num_particles', params['num_particles']))
        params['max_iterations'] = int(request.form.get('max_iterations', params['max_iterations']))
        params['inertia'] = float(request.form.get('inertia', params['inertia']))
        params['cognitive'] = float(request.form.get('cognitive', params['cognitive']))
        params['social'] = float(request.form.get('social', params['social']))
        params['is_maximization'] = request.form.get('is_maximization', str(params['is_maximization'])).lower() == 'on'

    # Parse and validate bounds
    try:
        lower, upper = map(float, bounds_input.split(','))
        params['bounds'] = [(lower, upper), (lower, upper)]  # Set bounds for both dimensions
    except ValueError:
        return jsonify({"error": "Invalid bounds format. Enter two numerical values separated by a comma."}), 400

    # Define the objective function
    objective_function_choice = request.form.get('objective_function_choice', 'quadratic')
    math_expr = None  # For rendering custom functions in math format

    if custom_function_code:
        # Handle custom function code provided via file upload
        try:
            def objective_function(variables):
                x, y = variables
                try:
                    return eval(custom_function_code, {"x": x, "y": y, "math": math})
                except Exception as e:
                    return jsonify({"error": f"Error evaluating the function: {str(e)}"}), 400

            if not callable(objective_function):
                raise ValueError("Custom function is not callable.")
        except Exception as e:
            return jsonify({"error": f"Error defining custom function: {str(e)}"}), 400
    elif objective_function_choice == 'custom':
        # Handle custom function defined in the form
        math_expr = request.form.get('math_expr')

        def objective_function(variables):
            x, y = variables
            try:
                return eval(math_expr, {"x": x, "y": y, "math": math})
            except Exception as e:
                return jsonify({"error": f"Error evaluating the function: {str(e)}"}), 400
    elif objective_function_choice in predefined_functions:
        # Use a predefined objective function
        objective_function = predefined_functions[objective_function_choice]
    else:
        return jsonify({"error": "Invalid objective function choice."}), 400

    # Run the PSO algorithm
    try:
        pso = PSO(
            objective_function,
            bounds=params['bounds'],
            num_particles=params['num_particles'],
            max_iterations=params['max_iterations'],
            is_maximization=params['is_maximization'],
            inertia=params['inertia'],
            cognitive=params['cognitive'],
            social=params['social']
        )
        pso.optimize()  # Perform optimization
    except Exception as e:
        return jsonify({"error": f"Error during PSO optimization: {str(e)}"}), 500

    # Generate output files and images
    text_file_path = create_text_file(pso, math_expr, custom_function_code)
    matplot_3d_img = create_3d_graph(pso.objective_function, pso.bounds, NUM_POINTS)
    matplot_animated_gif = create_animation(pso, NUM_POINTS)

    return jsonify(matplot_3d_img=matplot_3d_img, matplot_animated_gif=matplot_animated_gif, text_file_url=text_file_path)

@app.route('/download_best_particle_file', methods=['GET'])
def download_best_particle_file():
    """Provide a downloadable file containing the best particle's position."""
    text_file_path = request.args.get('file')  # Get file path from query parameters
    return send_file(text_file_path, as_attachment=True)  # Send file as an attachment

if __name__ == '__main__':
    app.run(debug=True)  # Start Flask app in debug mode
