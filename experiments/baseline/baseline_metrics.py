import json
from datetime import datetime

class BaselineMetrics:
    def __init__(self):
        self.baseline_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metrics': {
                'latency': {
                    'avg': 0,
                    'std': 0,
                    'min': 0,
                    'max': 0
                },
                'throughput': {
                    'avg': 0,
                    'std': 0,
                    'min': 0,
                    'max': 0
                },
                'resource_utilization': {
                    'avg': 0,
                    'std': 0,
                    'min': 0,
                    'max': 0
                },
                'recovery_time': {
                    'avg': 0,
                    'std': 0,
                    'min': 0,
                    'max': 0
                }
            }
        }
        
    def record_baseline(self, metrics_data):
        """记录基准数据"""
        self.baseline_data['metrics'] = metrics_data
        
    def save_baseline(self, filepath):
        """保存基准数据"""
        with open(filepath, 'w') as f:
            json.dump(self.baseline_data, f, indent=4)
            
    def load_baseline(self, filepath):
        """加载基准数据"""
        try:
            with open(filepath, 'r') as f:
                self.baseline_data = json.load(f)
        except FileNotFoundError:
            print("未找到基准数据文件")