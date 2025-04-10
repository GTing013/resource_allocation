import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd

class PerformanceVisualizer:
    def __init__(self, data_path):
        self.data_path = data_path
        
    def generate_dashboard(self, time_range='24h'):
        """生成性能面板"""
        data = self._load_data(time_range)
        if data.empty:
            return
            
        plt.figure(figsize=(15, 10))
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        titles = ['延迟趋势', '吞吐量趋势', '资源利用率', '恢复时间']
        
        for ax, metric, title in zip(axes.flat, metrics, titles):
            self._plot_metric(ax, data, metric, title)
            
        plt.tight_layout()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(f'/Users/huanghaoting/resource_allocation/monitoring/dashboard_{timestamp}.png')
        
    def _load_data(self, time_range):
        """加载数据"""
        df = pd.read_csv(self.data_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 根据时间范围筛选数据
        if time_range == '24h':
            start_time = datetime.now() - timedelta(hours=24)
        elif time_range == '7d':
            start_time = datetime.now() - timedelta(days=7)
        else:
            start_time = datetime.now() - timedelta(hours=1)
            
        return df[df['timestamp'] >= start_time]
        
    def _plot_metric(self, ax, data, metric, title):
        """绘制单个指标图表"""
        sns.lineplot(data=data, x='timestamp', y=metric, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('时间')
        ax.set_ylabel('值')
        ax.tick_params(axis='x', rotation=45)