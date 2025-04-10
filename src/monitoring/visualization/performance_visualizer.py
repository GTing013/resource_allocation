import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
import os

class PerformanceVisualizer:
    def __init__(self, data_path):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
        
    def generate_dashboard(self, time_range='24h'):
        """生成性能面板"""
        data = self._load_data(time_range)
        if data is None or data.empty:
            print("没有可用的监控数据")
            return
            
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        titles = ['延迟趋势', '吞吐量趋势', '资源利用率', '恢复时间']
        
        for ax, metric, title in zip(axes.flat, metrics, titles):
            self._plot_metric(ax, data, metric, title)
            
        plt.tight_layout()
        
        # 保存图表
        output_dir = os.path.join(self.data_path, 'dashboards')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(os.path.join(output_dir, f'dashboard_{timestamp}.png'))
        plt.close()
        
    def _load_data(self, time_range):
        """加载数据"""
        try:
            files = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]
            if not files:
                return None
                
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(self.data_path, x)))
            df = pd.read_csv(os.path.join(self.data_path, latest_file))
            
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # 根据时间范围筛选数据
                if time_range == '24h':
                    start_time = datetime.now() - timedelta(hours=24)
                elif time_range == '7d':
                    start_time = datetime.now() - timedelta(days=7)
                else:
                    start_time = datetime.now() - timedelta(hours=1)
                    
                return df[df['timestamp'] >= start_time]
            return df
            
        except Exception as e:
            print(f"加载数据失败: {e}")
            return None
        
    def _plot_metric(self, ax, data, metric, title):
        """绘制单个指标图表"""
        try:
            if metric in data.columns:
                sns.lineplot(data=data, x='timestamp', y=metric, ax=ax)
                ax.set_title(title)
                ax.set_xlabel('时间')
                ax.set_ylabel('值')
                ax.tick_params(axis='x', rotation=45)
            else:
                ax.text(0.5, 0.5, f'无{title}数据', 
                       horizontalalignment='center',
                       verticalalignment='center')
        except Exception as e:
            print(f"绘制{title}失败: {e}")