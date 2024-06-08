import os
import random
import datetime
from faker import Faker
import numpy as np

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

    def generate_distribution(self, log_count, num_distinct, distribution_type):
        print(f"Generating {distribution_type} distribution with {num_distinct} distinct values for {log_count} logs.")
        if distribution_type == "Normal":
            mean = log_count / num_distinct
            std_dev = mean / 2
            values = np.random.normal(loc=mean, scale=std_dev, size=num_distinct).astype(int)
        elif distribution_type == "Exponential":
            scale = log_count / num_distinct
            values = np.random.exponential(scale=scale, size=num_distinct).astype(int)
        else:  # Uniform
            values = np.full(num_distinct, log_count // num_distinct)
            values[:log_count % num_distinct] += 1

        # Adjust to ensure sum of values is equal to log_count
        while sum(values) > log_count:
            values[random.randint(0, num_distinct - 1)] -= 1
        while sum(values) < log_count:
            values[random.randint(0, num_distinct - 1)] += 1

        print(f"Distribution values: {values}")
        return values

    def generate_logs(self, entries, service_types, actions, num_destinations, dist_type_dest, num_users, dist_type_user, num_devices, dist_type_device, num_categories, dist_type_category):
        if not self.validate_choices(service_types, actions):
            raise ValueError("Please select at least one service type and one action.")

        time_span, log_count = entries[:2]
        min_sent, max_sent, avg_sent, min_received, max_received, avg_received = entries[2:8]

        # Generate unique destinations, users, devices, and categories
        destinations = [{
            "destinationIp": self.generate_ip(),
            "destinationPort": self.generate_port(),
            "destinationFQDN": self.generate_destination_fqdn()
        } for _ in range(num_destinations)]
        users = [{
            "userId": self.fake.uuid4(),
            "userPrincipalName": self.fake.email()
        } for _ in range(num_users)]
        devices = [{
            "deviceId": self.fake.uuid4(),
            "deviceOperatingSystem": self.fake.word(),
            "deviceOperatingSystemVersion": self.fake.word(),
            "deviceCategory": self.fake.word()
        } for _ in range(num_devices)]
        categories = [{
            "destinationWebCategory/displayName": self.fake.word()
        } for _ in range(num_categories)]

        # Generate distributions
        dist_dest = self.generate_distribution(log_count, num_destinations, dist_type_dest)
        dist_user = self.generate_distribution(log_count, num_users, dist_type_user)
        dist_device = self.generate_distribution(log_count, num_devices, dist_type_device)
        dist_category = self.generate_distribution(log_count, num_categories, dist_type_category)

        base_filename = os.path.join(self.config['default_directory'], "logs_output.txt")
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename[:-4]}_{counter}.txt"
            counter += 1

        logs = []

        # Create a list to track the indices for each distribution
        indices = {
            'dest': [i for i, count in enumerate(dist_dest) for _ in range(count)],
            'user': [i for i, count in enumerate(dist_user) for _ in range(count)],
            'device': [i for i, count in enumerate(dist_device) for _ in range(count)],
            'category': [i for i, count in enumerate(dist_category) for _ in range(count)]
        }



        for i in range(log_count):
            timestamp = self.generate_timestamp(self.config['time_span_options'][time_span])
            source_ip = self.generate_ip()
            destination = destinations[indices['dest'][i]]
            user = users[indices['user'][i]]
            device = devices[indices['device'][i]]
            category = categories[indices['category'][i]]
            bytes_sent = self.generate_bytes(min_sent, max_sent, avg_sent)
            bytes_received = self.generate_bytes(min_received, max_received, avg_received)
            service_type = self.fake.random_element(elements=[st for st, selected in zip(('Private', 'M365', 'Internet'), service_types) if selected])
            protocol = self.fake.random_element(elements=[pt for pt, selected in zip(('Tcp', 'Udp'), [True, True])])
            action = self.fake.random_element(elements=[ac for ac, selected in zip(('Allow', 'Block'), actions) if selected])

            log = f"{timestamp},{source_ip},{self.fake.uuid4()}:60707,{self.fake.uuid4()},{self.fake.uuid4()},{self.fake.uuid4()},,{service_type},'Client',{self.generate_ip()},1947,{destination['destinationFQDN']},{destination['destinationIp']},{destination['destinationPort']},'Windows 10 Business','10.0.19045',1.6.51,{device['deviceId']},{user['userId']},'{user['userPrincipalName']}',{protocol},'Ipv4',,,,,{bytes_sent},{bytes_received},,,,,,,,,,,,,,,,,,,,,,{timestamp},'Closed',,,,'{action}','QuickAccess',,'West US',,,,,,,,,,'Success',{timestamp},,{self.config['default_directory']},\n"
            logs.append(log)

        with open(filename, 'w') as file:
            file.writelines(logs)

