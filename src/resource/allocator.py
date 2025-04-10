import random
import time
from datetime import datetime, timedelta

class ResourceAllocator:
    def __init__(self):
        self.resources = {
            'cpu': {'total': 100, 'allocated': 0},
            'memory': {'total': 1024, 'allocated': 0}  # GB
        }
        
    def run_test(self, duration):
        """运行测试并收集性能数据"""
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=duration)
        
        test_data = {
            'latency_metrics': [],
            'throughput_metrics': [],
            'metrics': {
                'cpu_usage': [],
                'memory_usage': []
            },
            'failure_events': []
        }
        
        while datetime.now() < end_time:
            # 模拟资源使用
            cpu_usage = random.uniform(40, 90)
            memory_usage = random.uniform(50, 85)
            
            # 记录指标
            test_data['metrics']['cpu_usage'].append(cpu_usage)
            test_data['metrics']['memory_usage'].append(memory_usage)
            
            # 模拟延迟
            latency = random.uniform(100, 200)
            test_data['latency_metrics'].append(latency)
            
            # 模拟吞吐量
            throughput = random.uniform(500, 1000)
            test_data['throughput_metrics'].append(throughput)
            
            # 模拟故障事件
            if random.random() < 0.01:  # 1%的故障概率
                failure_time = datetime.now()
                recovery_time = failure_time + timedelta(seconds=random.uniform(30, 40))
                test_data['failure_events'].append({
                    'failure_time': failure_time.timestamp(),
                    'recovery_time': recovery_time.timestamp()
                })
            
            time.sleep(1)  # 每秒采样一次
            
        return test_data