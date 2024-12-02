import tempfile  # Module for creating temporary files


def parse_file(param_file, params):
    """
    Parse a parameter file and update parameters and custom function code.

    Args:
        param_file: The uploaded parameter file 
        params (dict): Default parameter dictionary to be updated.

    Returns:
        tuple: Updated parameters dictionary and custom function code as a string.
    """
    custom_function_code = None  # Initialize custom function code as None
    try:
        # Read the file and decode to UTF-8, then split into lines
        lines = param_file.read().decode('utf-8').splitlines()
        function_block = False  # Flag to indicate if reading a function block
        function_code_lines = []  # List to store lines of the function code

        for line in lines:
            # Start collecting function lines when 'function:' block is encountered
            if line.strip().lower() == 'function:':
                function_block = True
                continue

            if function_block:
                # Append lines to the function block
                function_code_lines.append(line)
            else:
                # Split key-value pairs and clean them
                key, value = line.split(":")
                key = key.strip().lower()
                value = value.strip()

                # Update the parameter dictionary based on keys
                if key in params:
                    if key == 'bounds':  # Handle bounds as string
                        params[key] = value
                    elif key in ['num_particles', 'max_iterations']:  # Convert integers
                        params[key] = int(value)
                    elif key in ['inertia', 'cognitive', 'social']:  # Convert floats
                        params[key] = float(value)
                    elif key == 'is_maximization':  # Handle boolean values
                        params[key] = value.lower() == 'true'

        if function_code_lines:
            # Combine all function lines into a single string
            custom_function_code = "\n".join(function_code_lines)

    except Exception as e:
        # Raise an error if parsing fails
        raise ValueError(f"Failed to parse the parameter file: {str(e)}")
    
    return params, custom_function_code  # Return updated parameters and custom function code

def create_text_file(pso, math_expr=None, custom_function_code=None):
    """
    Create a text file with simulation parameters and best positions for each iteration.

    Args:
        pso: A PSO (Particle Swarm Optimization) instance containing simulation data.
        math_expr (str, optional): math-formatted expression of the objective function.
        custom_function_code (str, optional): Custom Python code defining the objective function.

    Returns:
        str: Path to the created text file.
    """
    # Create a temporary text file
    text_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(text_file.name, 'w') as f:
        # Write simulation parameters
        f.write("Simulation Parameters:\n")
        f.write(f"Inertia: {pso.inertia}\n")
        f.write(f"Cognitive Coefficient: {pso.cognitive}\n")
        f.write(f"Social Coefficient: {pso.social}\n")
        f.write(f"Bounds: {pso.bounds}\n")
        f.write(f"Number of Particles: {pso.num_particles}\n")
        f.write(f"Max Iterations: {pso.max_iterations}\n")
        
        # Write the objective function definition
        if math_expr:
            f.write(f"Objective Function (math format): {math_expr}\n")
        elif custom_function_code:
            f.write(f"Objective Function (Custom Python code):\n{custom_function_code}\n")
        else:
            f.write(f"Objective Function: {str(pso.objective_function)}\n")
        
        # Write the optimization goal
        f.write(f"Optimization Goal: {'Maximization' if pso.is_maximization else 'Minimization'}\n\n")
        
        # Write the best particle positions per iteration
        f.write("Best Particle Positions per Iteration:\n")
        for i, best_position in enumerate(pso.best_positions_per_iteration):
            f.write(f"Iteration {i + 1}: {best_position}\n")
    
    # Return the file path
    return text_file.name
