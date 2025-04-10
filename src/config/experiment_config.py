class ExperimentConfig:
    def __init__(self):
        self.resource_configs = {
            'small': {
                'cpu': 2,
                'memory': '4Gi',
                'storage': '20Gi'
            },
            'medium': {
                'cpu': 4,
                'memory': '8Gi',
                'storage': '50Gi'
            },
            'large': {
                'cpu': 8,
                'memory': '16Gi',
                'storage': '100Gi'
            }
        }
        
        self.workload_patterns = {
            'constant': {'type': 'constant', 'value': 0.7},
            'random': {'type': 'random', 'min': 0.3, 'max': 0.9},
            'periodic': {'type': 'periodic', 'base': 0.6, 'amplitude': 0.3, 'period': 3600}
        }
        
        self.experiment_duration = 3600  # 1小时
        self.sampling_interval = 60      # 60秒