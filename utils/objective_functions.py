import math

def quadratic_function(variables):
    x, y = variables
    return x**2 + y**2

def sine_function(variables):
    x, y = variables
    return math.sin(x) + math.sin(y)

def exponential_decay(variables):
    x, y = variables
    return math.exp(-x**2 - y**2)

def logarithmic_function(variables):
    x, y = variables
    return math.log(x**2 + y**2 + 1)

def rastrigin_function(variables):
    x, y = variables
    return 20 + x**2 + y**2 - 10 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))

def ackley_function(variables):
    x, y = variables
    return -20 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2))) - math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) + math.e + 20

# Mapping of function names to functions
predefined_functions = {
    'quadratic': quadratic_function,
    'sine': sine_function,
    'exponential_decay': exponential_decay,
    'logarithmic': logarithmic_function,
    'rastrigin': rastrigin_function,
    'ackley': ackley_function
}
