import unittest
from collections import Counter
from faker import Faker
import numpy as np
from logs_generator.backend.log_generator import LogGenerator

class TestLogGenerator(unittest.TestCase):
    def setUp(self):
        self.config = {
            'default_directory': './logs',
            'time_span_options': [24, 48, 72]
        }
        self.log_generator = LogGenerator(self.config)
        self.entries = [0, 100, 100, 1000, 500, 200, 700, 300]  # example entries
        self.service_types = [True, True, False]  # example service types
        self.actions = [True, True]  # example actions
        self.num_destinations = 10  # example number of destinations
        self.users = [Faker().uuid4() for _ in range(10)]  # example users
        self.devices = [Faker().uuid4() for _ in range(10)]  # example devices
        self.categories = [Faker().word() for _ in range(5)]  # example categories

    def check_distribution(self, distribution, log_count):
        self.assertEqual(sum(distribution), log_count)
        self.assertTrue(all(n >= 0 for n in distribution))

    def test_uniform_distribution_destinations(self):
        distribution = self.log_generator.generate_distribution(100, 10, "Uniform")
        self.check_distribution(distribution, 100)
        count = Counter(distribution)
        self.assertTrue(all(count[val] > 0 for val in count))  # Check if all values are represented

    def test_exponential_distribution_destinations(self):
        distribution = self.log_generator.generate_distribution(100, 10, "Exponential")
        self.check_distribution(distribution, 100)
        self.assertGreater(max(distribution), min(distribution))  # Ensure the distribution is varied

    def test_normal_distribution_destinations(self):
        distribution = self.log_generator.generate_distribution(100, 10, "Normal")
        self.check_distribution(distribution, 100)
        self.assertGreater(max(distribution), min(distribution))  # Ensure the distribution is varied

    def test_uniform_distribution_users(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        user_counts = Counter(log.split(',')[17] for log in logs)
        self.assertTrue(all(count > 0 for count in user_counts.values()))  # Ensure all users are represented

    def test_exponential_distribution_users(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        user_counts = Counter(log.split(',')[17] for log in logs)
        self.assertGreater(max(user_counts.values()), min(user_counts.values()))  # Ensure the distribution is varied

    def test_normal_distribution_users(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        user_counts = Counter(log.split(',')[17] for log in logs)
        self.assertGreater(max(user_counts.values()), min(user_counts.values()))  # Ensure the distribution is varied

    def test_uniform_distribution_devices(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        device_counts = Counter(log.split(',')[18] for log in logs)
        self.assertTrue(all(count > 0 for count in device_counts.values()))  # Ensure all devices are represented

    def test_exponential_distribution_devices(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        device_counts = Counter(log.split(',')[18] for log in logs)
        self.assertGreater(max(device_counts.values()), min(device_counts.values()))  # Ensure the distribution is varied

    def test_normal_distribution_devices(self):
        self.log_generator.generate_logs(self.entries, self.service_types, self.actions, self.num_destinations, self.users, self.devices, self.categories)
        with open('./logs/logs_output.txt') as f:
            logs = f.readlines()
        device_counts = Counter(log.split(',')[18] for log in logs)
        self.assertGreater(max(device_counts.values()), min(device_counts.values()))  # Ensure the distribution is varied

if __name__ == '__main__':
    unittest.main()
