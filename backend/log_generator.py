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
        return "98c58e9d-dae2-497a-82ab-898f106bca48"

    def generate_timestamp(self, hours):
        return (datetime.datetime.now() - datetime.timedelta(hours=random.randint(0, hours))).strftime('%Y-%m-%dT%H:%M:%SZ')

    def generate_destination_fqdn(self):
        return self.fake.domain_name()

    def generate_bytes(self, min_val, max_val, avg_val):
        return int(random.triangular(min_val, max_val, avg_val)) if random.random() < 0.5 else random.randint(min_val, max_val)

    def validate_choices(self, *args):
        return all(any(choices) for choices in args)

    def generate_logs(self, entries, service_types, actions):
        if not self.validate_choices(service_types, actions):
            raise ValueError("Please select at least one service type and one action.")

        time_span, log_count = entries[:2]
        min_sent, max_sent, avg_sent, min_received, max_received, avg_received = entries[2:8]
        num_destinations, dest_dist_type = entries[8], entries[9]
        num_users, user_dist_type = entries[10], entries[11]
        num_devices, device_dist_type = entries[12], entries[13]
        num_categories, category_dist_type = entries[14], entries[15]

        destinations = [self.generate_destination_fqdn() for _ in range(num_destinations)]
        users = [self.fake.uuid4() for _ in range(num_users)]
        devices = [self.fake.uuid4() for _ in range(num_devices)]
        categories = [self.fake.word() for _ in range(num_categories)]

        base_filename = os.path.join(self.config['default_directory'], "logs_output.txt")
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename[:-4]}_{counter}.txt"
            counter += 1

        with open(filename, 'w') as file:
            for _ in range(log_count):
                timestamp = self.generate_timestamp(self.config['time_span_options'][time_span])
                source_ip = self.generate_ip()
                dest = random.choice(destinations)
                user = random.choice(users)
                device = random.choice(devices)
                category = random.choice(categories)
                bytes_sent = self.generate_bytes(min_sent, max_sent, avg_sent)
                bytes_received = self.generate_bytes(min_received, max_received, avg_received)
                service_type = self.fake.random_element(elements=[st for st, selected in zip(('Private', 'M365', 'Internet'), service_types) if selected])
                protocol = self.fake.random_element(elements=[pt for pt, selected in zip(('Tcp', 'Udp'), [True, True])])
                action = self.fake.random_element(elements=[ac for ac, selected in zip(('Allow', 'Block'), actions) if selected])

                log = f"{timestamp},{source_ip},{self.fake.uuid4()}:60707,{self.fake.uuid4()},{self.fake.uuid4()},{self.fake.uuid4()},,{service_type},'Client',{self.generate_ip()},1947,{dest},{self.generate_ip()},60707,'Windows 10 Business','10.0.19045',1.6.51,{device},{user},'{self.fake.email()}',{protocol},'Ipv4',,,,,{bytes_sent},{bytes_received},,,,,,,,,,,,,,,,,,,,,,{timestamp},'Closed',,,,'{action}','QuickAccess',,'West US',,,,,,,,,,'Success',{timestamp},,{self.config['default_directory']}\n"
                file.write(log)
