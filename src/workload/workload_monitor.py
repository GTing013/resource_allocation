import psutil
import time
from datetime import datetime
import logging

class WorkloadMonitor:
    def __init__(self, workload_manager):
        self.workload_manager = workload_manager
        self.logger = logging.getLogger(__name__)
        self.monitoring_interval = 5  # 秒
        self.alert_manager = AlertManager()
        self.autoscaler = AutoScaler(ResourceLimiter())
        
    def start_monitoring(self, workload_id):
        """开始监控工作负载"""
        try:
            while True:
                metrics = self._collect_metrics(workload_id)
                self._update_workload_metrics(workload_id, metrics)
                
                # 检查告警
                self.alert_manager.check_alerts(workload_id, metrics)
                
                # 检查自动扩缩容
                self.autoscaler.check_and_scale(workload_id, metrics)
                
                time.sleep(self.monitoring_interval)
                
        except Exception as e:
            self.logger.error(f"监控工作负载 {workload_id} 失败: {e}")
            
    def _collect_metrics(self, workload_id):
        """收集工作负载指标"""
        try:
            # 获取系统资源使用情况
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            return {
                'timestamp': datetime.now(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'io_counters': psutil.disk_io_counters()
            }
        except Exception as e:
            self.logger.error(f"收集指标失败: {e}")
            return None
            
    def _update_workload_metrics(self, workload_id, metrics):
        """更新工作负载指标"""
        if not metrics:
            return
            
        workload = self.workload_manager.workloads.get(workload_id)
        if workload:
            workload['metrics']['cpu_usage'].append(metrics['cpu_usage'])
            workload['metrics']['memory_usage'].append(metrics['memory_usage'])
            
            # 保持最近100个数据点
            if len(workload['metrics']['cpu_usage']) > 100:
                workload['metrics']['cpu_usage'] = workload['metrics']['cpu_usage'][-100:]
                workload['metrics']['memory_usage'] = workload['metrics']['memory_usage'][-100:]
                
    def _check_anomalies(self, workload_id, metrics):
        """检查异常情况"""
        if not metrics:
            return False
            
        # 定义阈值
        thresholds = {
            'cpu_usage': 90,
            'memory_usage': 90
        }
        
        return (metrics['cpu_usage'] > thresholds['cpu_usage'] or
                metrics['memory_usage'] > thresholds['memory_usage'])
                
    def _handle_anomaly(self, workload_id):
        """处理异常情况"""
        self.logger.warning(f"工作负载 {workload_id} 出现异常")
        self.workload_manager.update_workload_status(
            workload_id, 
            'warning',
            '资源使用超过阈值'
        )