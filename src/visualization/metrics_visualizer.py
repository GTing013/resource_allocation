import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class MetricsVisualizer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_dashboard(self, workload_id, metrics_data, analysis_results):
        """生成监控面板"""
        plt.style.use('seaborn')
        fig = plt.figure(figsize=(15, 10))
        
        # 创建子图
        gs = fig.add_gridspec(3, 2)
        
        # CPU使用率趋势
        self._plot_metric_trend(fig.add_subplot(gs[0, :]), 
                              metrics_data, 'cpu_usage', 'CPU使用率趋势')
        
        # 内存使用率趋势
        self._plot_metric_trend(fig.add_subplot(gs[1, :]), 
                              metrics_data, 'memory_usage', '内存使用率趋势')
        
        # 统计信息
        self._plot_stats(fig.add_subplot(gs[2, 0]), analysis_results['basic_stats'])
        
        # 异常检测结果
        self._plot_anomalies(fig.add_subplot(gs[2, 1]), analysis_results['anomalies'])
        
        # 保存图表
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(f'{self.output_dir}/dashboard_{workload_id}_{timestamp}.png')
        plt.close()
        
    def _plot_metric_trend(self, ax, data, metric, title):
        """绘制指标趋势图"""
        sns.lineplot(data=data, x='timestamp', y=metric, ax=ax)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
        
    def _plot_stats(self, ax, stats):
        """绘制统计信息"""
        metrics = list(stats.keys())
        values = [stats[m]['mean'] for m in metrics]
        
        sns.barplot(x=metrics, y=values, ax=ax)
        ax.set_title('平均资源使用率')
        
    def _plot_anomalies(self, ax, anomalies):
        """绘制异常检测结果"""
        metrics = list(anomalies.keys())
        counts = [anomalies[m]['count'] for m in metrics]
        
        sns.barplot(x=metrics, y=counts, ax=ax)
        ax.set_title('异常值统计')