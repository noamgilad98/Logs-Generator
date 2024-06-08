import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logs_generator.frontend.application_gui import ApplicationGUI
from logs_generator.backend.config_manager import ConfigManager
from logs_generator.backend.log_generator import LogGenerator
import tkinter as tk
from unittest.mock import patch, MagicMock

class TestLogGenerator(unittest.TestCase):
    def setUp(self):
        self.config = {
            'default_directory': 'test_logs',
            'time_span_options': [24, 48, 72]
        }
        self.log_generator = LogGenerator(self.config)
        if not os.path.exists('test_logs'):
            os.makedirs('test_logs')

    def tearDown(self):
        if os.path.exists('test_logs/logs_output.txt'):
            os.remove('test_logs/logs_output.txt')
        if os.path.exists('test_logs'):
            os.rmdir('test_logs')

    def test_uniform_distribution_10_logs_8_destinations(self):
        entries = [0, 10, 100, 200, 150, 100, 200, 150]  # Example values for time_span, log_count, and bytes
        service_types = [True, False, False]  # Only 'Private' service type selected
        actions = [True, False]  # Only 'Allow' action selected

        num_destinations = 8
        dist_type_dest = "Uniform"
        num_users = 10
        dist_type_user = "Uniform"
        num_devices = 10
        dist_type_device = "Uniform"
        num_categories = 10
        dist_type_category = "Uniform"

        fake = MagicMock()
        fake.domain_name.side_effect = [f'dest{i}.com' for i in range(num_destinations)]
        fake.uuid4.side_effect = [f'user{i}' for i in range(num_users)] + [f'device{i}' for i in range(num_devices)] + [f'cat{i}' for i in range(num_categories)]

        with patch('logs_generator.backend.log_generator.Faker', return_value=fake):
            self.log_generator.generate_logs(entries, service_types, actions, num_destinations, dist_type_dest, num_users, dist_type_user, num_devices, dist_type_device, num_categories, dist_type_category)

        with open('test_logs/logs_output.txt', 'r') as file:
            logs = file.readlines()

        destinations = [log.split(',')[12] for log in logs]  # Extracting destinationFQDN from logs
        dest_counts = {dest: destinations.count(dest) for dest in set(destinations)}

        expected_counts = [1, 1, 1, 1, 1, 1, 2, 2]
        actual_counts = sorted(dest_counts.values())

        self.assertTrue(expected_counts == actual_counts)

class TestSimpleAssertion(unittest.TestCase):
    def test_true_equals_true(self):
        self.assertTrue(True)

if __name__ == "__main__":
    root = tk.Tk()
    config_manager = ConfigManager("config.json")
    config = config_manager.config
    log_generator = LogGenerator(config)
    app = ApplicationGUI(root, config_manager, log_generator)
    unittest.main()
