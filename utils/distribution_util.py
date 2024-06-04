import numpy as np

def generate_distribution(num_elements, distribution_type):
    values = np.linspace(0, num_elements, num=1000)
    if distribution_type == "Normal":
        mean = num_elements / 2
        std_dev = mean / 3
        values = np.random.normal(loc=mean, scale=std_dev, size=1000)
    elif distribution_type == "Uniform":
        values = np.random.uniform(low=0, high=num_elements, size=1000)
    elif distribution_type == "Exponential":
        values = np.random.exponential(scale=num_elements / 5, size=1000)
    return np.clip(np.round(values).astype(int), 0, num_elements - 1)
