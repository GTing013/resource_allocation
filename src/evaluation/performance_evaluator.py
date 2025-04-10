import pandas as pd
import matplotlib.pyplot as plt

class PerformanceEvaluator:
    def __init__(self):
        self.metrics_history = []

    def record_metrics(self, metrics):
        self.metrics_history.append({
            'timestamp': pd.Timestamp.now(),
            **metrics
        })

    def calculate_statistics(self):
        df = pd.DataFrame(self.metrics_history)
        return {
            'avg_latency': df['latency'].mean(),
            'throughput': df['throughput'].mean(),
            'resource_utilization': df['resource_utilization'].mean(),
            'sla_violations': self._calculate_sla_violations(df)
        }

    def plot_metrics(self):
        df = pd.DataFrame(self.metrics_history)
        
        # 绘制性能指标图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        df.plot(x='timestamp', y='latency', ax=axes[0,0])
        df.plot(x='timestamp', y='throughput', ax=axes[0,1])
        df.plot(x='timestamp', y='resource_utilization', ax=axes[1,0])
        plt.tight_layout()
        plt.savefig('performance_metrics.png')