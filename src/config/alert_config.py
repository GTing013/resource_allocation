class AlertConfig:
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-app-password',
            'recipients': ['admin@example.com']
        }
        
        self.alert_thresholds = {
            'latency': {'warning': 150, 'critical': 200},
            'throughput': {'warning': 700, 'critical': 500},
            'resource_utilization': {'warning': 0.8, 'critical': 0.9},
            'recovery_time': {'warning': 35, 'critical': 45}
        }
        
        self.alert_channels = ['email', 'console']