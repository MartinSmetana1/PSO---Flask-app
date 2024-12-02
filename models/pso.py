import numpy as np
from .particle import Particle

class PSO:
    """Performs Particle Swarm Optimization (PSO) based on provided parameters and objective function."""

    def __init__(self, objective_function, bounds, num_particles, max_iterations, 
                 is_maximization, inertia=0.6, cognitive=0.5, social=2, max_velocity=2.0):
        """
        Initializes the PSO algorithm with given parameters.

        Args:
            objective_function: The function to optimize (minimization or maximization).
            bounds: A list of tuples defining the bounds for each dimension of the search space.
            num_particles: The number of particles (agents) in the swarm.
            max_iterations: The maximum number of iterations to run the optimization.
            is_maximization: Whether to perform maximization (True) or minimization (False).
            inertia: Weight for the previous velocity (controls how much particles rely on past velocity).
            cognitive: Weight for the particle's own best position (controls exploration).
            social: Weight for the best position of the global swarm (controls exploitation).
            max_velocity: The maximum speed particles can move at.
        """
        # Store the function to optimize and other parameters
        self.objective_function = objective_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.is_maximization = is_maximization  # Whether the objective function is maximized
        self.inertia = inertia  # Controls how much previous velocity influences the particle's next move
        self.cognitive = cognitive  # Controls how much a particle is influenced by its own experience
        self.social = social  # Controls how much a particle is influenced by the best swarm position
        self.max_velocity = max_velocity  # The maximum speed a particle can have
        
        # Initialize the global best position randomly within the bounds
        self.global_best_position = np.random.uniform(
            low=[lower for lower, _ in bounds], high=[upper for _, upper in bounds]
        )
        
        # Set the global best score based on the optimization type (maximization or minimization)
        self.global_best_score = float('-inf') if is_maximization else float('inf')
        
        # Create a list of particles in the swarm
        self.particles = [Particle(bounds) for _ in range(num_particles)]
        
        # Initialize the history of particle positions and best positions
        self.history = []
        self.best_positions_per_iteration = []
        

    def optimize(self):
        """Runs the PSO optimization for the set number of iterations."""
        #print(self.is_maximization)

        for iteration in range(self.max_iterations):
            iteration_positions = []  # To store the positions of particles at each iteration
           # print(f"Starting iteration {iteration + 1}/{self.max_iterations}")
            #print(self.objective_function)    
            # Loop over each particle in the swarm
            for particle in self.particles:
                # Evaluate the particle's current position using the objective function
                #print(f"Particle position: {particle.position}")
                score = self.objective_function(particle.position)
                

                # If this score is better than the particle's personal best, update its best score and position
                if (self.is_maximization and score > particle.best_score) or \
                   (not self.is_maximization and score < particle.best_score):
                    particle.best_score = score
                    particle.best_position = particle.position.copy()

                # If this score is better than the global best, update the global best score and position
                if (self.is_maximization and score > self.global_best_score) or \
                   (not self.is_maximization and score < self.global_best_score):
                    self.global_best_score = score
                    self.global_best_position = particle.position.copy()

                # Update the particle's velocity using the inertia, cognitive, and social components
                inertia_component = self.inertia * particle.velocity  # Particle's previous velocity
                cognitive_component = self.cognitive * np.random.rand(len(self.bounds)) * (particle.best_position - particle.position)  # Particle's attraction to its own best position
                social_component = self.social * np.random.rand(len(self.bounds)) * (self.global_best_position - particle.position)  # Attraction to global best position
                momentum_component = 0.01 * particle.velocity if self.is_maximization else 0  # Optional momentum term for maximization
                
                # Combine the components to update the particle's velocity
                particle.velocity = inertia_component + cognitive_component + social_component + momentum_component

                # Update the particle's position based on its new velocity
                particle.position += particle.velocity

                # Ensure the particle stays within the defined bounds (clamp position)
                particle.position = np.clip(particle.position, [lower for lower, _ in self.bounds], [upper for _, upper in self.bounds])
                
                # Store the updated particle position for this iteration
                iteration_positions.append(particle.position.copy())

            # Add the positions of all particles in this iteration to the history
            self.history.append(np.array(iteration_positions))
            
            # Record the global best position after this iteration
            self.best_positions_per_iteration.append(self.global_best_position.copy())
           # print(f"Global best position after iteration {iteration + 1}: {self.global_best_position}")

            # Gradually reduce the inertia over time to reduce exploration and increase exploitation
            #self.inertia = max(1, self.inertia * 0.99)  # Inertia decreases with each iteration
