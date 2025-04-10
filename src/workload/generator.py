import numpy as np

class WorkloadGenerator:
    def __init__(self, pattern_type='random'):
        self.pattern_type = pattern_type
        
    def generate_workload(self, duration, interval):
        if self.pattern_type == 'random':
            return self._generate_random_workload(duration, interval)
        elif self.pattern_type == 'periodic':
            return self._generate_periodic_workload(duration, interval)
        elif self.pattern_type == 'burst':
            return self._generate_burst_workload(duration, interval)
            
    def _generate_random_workload(self, duration, interval):
        timestamps = np.arange(0, duration, interval)
        load = np.random.normal(0.6, 0.2, len(timestamps))
        return timestamps, np.clip(load, 0, 1)