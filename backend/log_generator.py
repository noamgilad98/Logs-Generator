from collections import Counter
import random
import datetime
from faker import Faker
import numpy as np
import os

class LogGenerator:
    def __init__(self, config):
        self.config = config
        self.fake = Faker()
        self.ensure_directory()

    def ensure_directory(self):
        if not os.path.exists(self.config['default_directory']):
            os.makedirs(self.config['default_directory'])

    def generate_ip(self):
        return "98c58e9d-dae2-497a-82ab-898f106bca48"

    def generate_timestamp(self, hours):
        return (datetime.datetime.now() - datetime.timedelta(hours=random.randint(0, hours))).strftime('%Y-%m-%dT%H:%M:%SZ')

    def generate_destination_fqdn(self):
        return self.fake.domain_name()

    def generate_bytes(self, min_val, max_val, avg_val):
        return int(random.triangular(min_val, max_val, avg_val)) if random.random() < 0.5 else random.randint(min_val, max_val)

    def validate_choices(self, *args):
        return all(any(choices) for choices in args)

    def generate_distribution(self, count, dist_type):
        if dist_type == "Normal":
            mean = count / 2
            std_dev = mean / 3
            values = np.random.normal(loc=mean, scale=std_dev, size=count)
        elif dist_type == "Uniform":
            values = np.random.uniform(low=0, high=count, size=count)
        elif dist_type == "Exponential":
            values = np.random.exponential(scale=count / 5, size=count)
        return values

    def generate_logs(self, entries, service_types, actions):
        if not self.validate_choices(service_types, actions):
            raise ValueError("Please select at least one service type and one action.")

        time_span, log_count, min_sent, max_sent, avg_sent, min_received, max_received, avg_received, num_destinations, dist_dest, num_users, dist_users, num_devices, dist_devices, num_categories, dist_categories = entries

        dest_values = self.generate_distribution(num_destinations, dist_dest)
        user_values = self.generate_distribution(num_users, dist_users)
        device_values = self.generate_distribution(num_devices, dist_devices)
        category_values = self.generate_distribution(num_categories, dist_categories)

        dest_indices = np.clip(np.round(dest_values).astype(int), 0, num_destinations - 1)
        user_indices = np.clip(np.round(user_values).astype(int), 0, num_users - 1)
        device_indices = np.clip(np.round(device_values).astype(int), 0, num_devices - 1)
        category_indices = np.clip(np.round(category_values).astype(int), 0, num_categories - 1)

        destination_counts = Counter(dest_indices)
        user_counts = Counter(user_indices)
        device_counts = Counter(device_indices)
        category_counts = Counter(category_indices)

        base_filename = os.path.join(self.config['default_directory'], "logs_output.txt")
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename[:-4]}_{counter}.txt"
            counter += 1

        with open(filename, 'w') as file:
            for index, count in destination_counts.items():
                dest = f"destination_{index}"
                for _ in range(count):
                    timestamp = self.generate_timestamp(self.config['time_span_options'][time_span])
                    source_ip = self.generate_ip()
                    bytes_sent = self.generate_bytes(min_sent, max_sent, avg_sent)
                    bytes_received = self.generate_bytes(min_received, max_received, avg_received)
                    service_type = self.fake.random_element(elements=[st for st, selected in zip(('Private', 'M365', 'Internet'), service_types) if selected])
                    protocol = self.fake.random_element(elements=[pt for pt, selected in zip(('Tcp', 'Udp'), [True, True])])
                    action = self.fake.random_element(elements=[ac for ac, selected in zip(('Allow', 'Block'), actions) if selected])

                    log = f"{timestamp},{source_ip},{self.fake.uuid4()}:60707,{self.fake.uuid4()},{self.fake.uuid4()},{self.fake.uuid4()},,{service_type},'Client',{self.generate_ip()},1947,{dest},{self.generate_ip()},60707,'Windows 10 Business','10.0.19045',1.6.51,{self.fake.uuid4()},{self.fake.uuid4()},'{self.fake.email()}',{protocol},'Ipv4',,,,,{bytes_sent},{bytes_received},,,,,,,,,,,,,,,,,,,,,,{timestamp},'Closed',,,,'{action}','QuickAccess',,'West US',,,,,,,,,,'Success',{timestamp},,{self.config['default_directory']}\n"
                    file.write(log)
