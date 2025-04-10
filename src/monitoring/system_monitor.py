import time
from datetime import datetime
import pandas as pd
from monitoring.alert.alert_manager import AlertManager
from monitoring.visualization.performance_visualizer import PerformanceVisualizer

class SystemMonitor:
    def __init__(self, metrics_collector, alert_threshold=0.2):
        self.metrics_collector = metrics_collector
        self.alert_threshold = alert_threshold
        self.baseline_metrics = None
        self.monitoring_data = []
        self.alert_manager = AlertManager()
        self.visualizer = PerformanceVisualizer('/Users/huanghaoting/resource_allocation/monitoring/data')
        
    def start_monitoring(self, interval=60):
        """开始系统监控"""
        print("开始系统监控...")
        
        # 初始化基准指标
        if self.baseline_metrics is None:
            initial_metrics = self.metrics_collector.collect_metrics()
            self.baseline_metrics = initial_metrics
            print("基准指标已设置")
        
        while True:
            try:
                # 收集当前指标
                current_metrics = self.metrics_collector.collect_metrics()
                
                # 检查性能退化
                degradation = self._check_performance_degradation(current_metrics)
                if degradation:
                    self._send_alert(degradation)
                
                # 记录监控数据
                self._record_metrics(current_metrics)
                
                # 更新可视化面板
                if self._should_update_dashboard():
                    self.visualizer.generate_dashboard()
                    print("已更新性能面板")
                
                # 每天更新基准指标
                self._update_baseline_if_needed()
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"监控错误: {e}")
                time.sleep(5)
    
    def _update_baseline_if_needed(self):
        """定期更新基准指标"""
        if not self.monitoring_data:
            return
            
        last_update = self.monitoring_data[0].get('timestamp')
        if last_update and (datetime.now() - last_update).days >= 1:
            # 使用最近24小时的数据计算新的基准
            recent_data = pd.DataFrame(self.monitoring_data[-1440:])  # 假设每分钟一条数据
            self.baseline_metrics = {
                metric: recent_data[metric].mean()
                for metric in ['latency', 'throughput', 'resource_utilization', 'recovery_time']
                if metric in recent_data.columns
            }
            print("基准指标已更新")
    
    def _should_update_dashboard(self):
        """检查是否需要更新面板"""
        if not self.monitoring_data:
            return False
            
        last_record = self.monitoring_data[-1]
        current_time = datetime.now()
        last_time = last_record['timestamp']
        
        return current_time.hour != last_time.hour
    
    def _send_alert(self, degradation):
        """发送告警"""
        self.alert_manager.send_alert(degradation)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_msg = f"[{timestamp}] 性能退化警告:\n"
        
        for metric, change in degradation.items():
            direction = "上升" if change > 0 else "下降"
            percentage = abs(change) * 100
            alert_msg += f"- {metric}: {direction} {percentage:.1f}%\n"
            
        # TODO: 实现具体的告警方式（邮件、短信等）
        print(alert_msg)
    
    def _analyze_degradation(self, df):
        """分析性能退化情况"""
        events = []
        metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        
        for metric in metrics:
            if metric in df.columns:
                mean = df[metric].mean()
                std = df[metric].std()
                outliers = df[df[metric] > mean + 2 * std]
                
                if not outliers.empty:
                    events.append(f"{metric} 出现异常值: {len(outliers)} 次")
                    
        return events