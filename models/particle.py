import numpy as np

class Particle:
    """Represents a single particle in the PSO algorithm with position, velocity, and best-known state."""

    def __init__(self, bounds):
        """
        Initializes a particle with a random position and velocity.
        
        Args:
            bounds (list of tuples): The bounds for each dimension of the particle's position. 
                                      Each tuple is (lower_bound, upper_bound).
        """
        # Generate random position within the provided bounds for each dimension
        self.position = np.array([np.random.uniform(lower, upper) for lower, upper in bounds])
        
        # Initialize velocity with random values between -0.1 and 0.1 for each dimension
        self.velocity = np.random.uniform(-0.1, 0.1, len(bounds))
        
        # The best known position of this particle (initially its starting position)
        self.best_position = self.position.copy()
        
        # The best known score (fitness value) of this particle (initially set to infinity)
        self.best_score = float('inf')
