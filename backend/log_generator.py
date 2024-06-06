import os
import random
import datetime
from faker import Faker
import numpy as np
from collections import Counter

class LogGenerator:
    def __init__(self, config):
        self.config = config
        self.fake = Faker()
        self.ensure_directory()

    def ensure_directory(self):
        if not os.path.exists(self.config['default_directory']):
            os.makedirs(self.config['default_directory'])

    def generate_ip(self):
        return self.fake.ipv4()

    def generate_port(self):
        return random.randint(1024, 65535)

    def generate_timestamp(self, hours):
        return (datetime.datetime.now() - datetime.timedelta(hours=random.randint(0, hours))).strftime('%Y-%m-%dT%H:%M:%SZ')

    def generate_destination_fqdn(self):
        return self.fake.domain_name()

    def generate_bytes(self, min_val, max_val, avg_val):
        return int(random.triangular(min_val, max_val, avg_val)) if random.random() < 0.5 else random.randint(min_val, max_val)

    def validate_choices(self, *args):
        return all(any(choices) for choices in args)

    def generate_distribution(self, log_count, num_destinations, distribution_type):
        if distribution_type == "Normal":
            mean = log_count / num_destinations
            std_dev = mean / 2
            distribution = np.random.normal(loc=mean, scale=std_dev, size=num_destinations).astype(int)
        elif distribution_type == "Exponential":
            scale = log_count / num_destinations
            distribution = np.random.exponential(scale=scale, size=num_destinations).astype(int)
        else:  # Uniform
            distribution = np.full(num_destinations, log_count // num_destinations)
            distribution[:log_count % num_destinations] += 1

        # Ensure no negative values and adjust to match log_count
        distribution = np.clip(distribution, 0, None)
        while distribution.sum() > log_count:
            distribution[random.randint(0, num_destinations - 1)] -= 1
        while distribution.sum() < log_count:
            distribution[random.randint(0, num_destinations - 1)] += 1

        return distribution

    def generate_logs(self, entries, service_types, actions, num_destinations, users, devices, categories, distribution_type):
        if not self.validate_choices(service_types, actions):
            raise ValueError("Please select at least one service type and one action.")

        time_span, log_count = entries[:2]
        min_sent, max_sent, avg_sent, min_received, max_received, avg_received = entries[2:8]

        # Generate unique destinations
        destinations = [{
            "destinationIp": self.generate_ip(),
            "destinationPort": self.generate_port(),
            "destinationFQDN": self.generate_destination_fqdn()
        } for _ in range(num_destinations)]

        # Generate distribution of logs per destination
        distribution = self.generate_distribution(log_count, num_destinations, distribution_type)

        base_filename = os.path.join(self.config['default_directory'], "logs_output.txt")
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename[:-4]}_{counter}.txt"
            counter += 1

        logs = []

        for dest_index, num_logs_for_this_dest in enumerate(distribution):
            destination = destinations[dest_index]
            for _ in range(num_logs_for_this_dest):
                timestamp = self.generate_timestamp(self.config['time_span_options'][time_span])
                source_ip = self.generate_ip()
                user = random.choice(users)
                device = random.choice(devices)
                category = random.choice(categories)
                bytes_sent = self.generate_bytes(min_sent, max_sent, avg_sent)
                bytes_received = self.generate_bytes(min_received, max_received, avg_received)
                service_type = self.fake.random_element(elements=[st for st, selected in zip(('Private', 'M365', 'Internet'), service_types) if selected])
                protocol = self.fake.random_element(elements=[pt for pt, selected in zip(('Tcp', 'Udp'), [True, True])])
                action = self.fake.random_element(elements=[ac for ac, selected in zip(('Allow', 'Block'), actions) if selected])

                log = f"{timestamp},{source_ip},{self.fake.uuid4()}:60707,{self.fake.uuid4()},{self.fake.uuid4()},{self.fake.uuid4()},,{service_type},'Client',{self.generate_ip()},1947,{destination['destinationFQDN']},{destination['destinationIp']},{destination['destinationPort']},'Windows 10 Business','10.0.19045',1.6.51,{device},{user},'{self.fake.email()}',{protocol},'Ipv4',,,,,{bytes_sent},{bytes_received},,,,,,,,,,,,,,,,,,,,,,{timestamp},'Closed',,,,'{action}','QuickAccess',,'West US',,,,,,,,,,'Success',{timestamp},,{self.config['default_directory']}\n"
                logs.append(log)

        with open(filename, 'w') as file:
            file.writelines(logs)
