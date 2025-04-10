import psutil
import time
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.metrics_cache = {}
        self.cache_duration = 60  # 缓存时间（秒）
        
    def collect_metrics(self):
        """收集系统性能指标"""
        current_time = time.time()
        
        # 如果缓存有效，直接返回缓存数据
        if self.metrics_cache and current_time - self.metrics_cache.get('timestamp', 0) < self.cache_duration:
            return self.metrics_cache['data']
            
        metrics = {
            'latency': self._collect_latency(),
            'throughput': self._collect_throughput(),
            'resource_utilization': self._collect_resource_utilization(),
            'recovery_time': self._collect_recovery_time()
        }
        
        # 更新缓存
        self.metrics_cache = {
            'timestamp': current_time,
            'data': metrics
        }
        
        return metrics
        
    def _collect_latency(self):
        """收集延迟数据"""
        return psutil.cpu_percent(interval=1)  # 使用CPU使用率作为延迟指标
        
    def _collect_throughput(self):
        """收集吞吐量数据"""
        net_io = psutil.net_io_counters()
        return (net_io.bytes_sent + net_io.bytes_recv) / 1024  # KB/s
        
    def _collect_resource_utilization(self):
        """收集资源利用率"""
        memory = psutil.virtual_memory()
        return memory.percent / 100  # 转换为0-1范围
        
    def _collect_recovery_time(self):
        """收集恢复时间"""
        # 模拟恢复时间数据
        return 30 + (psutil.cpu_percent() / 100) * 10  # 基础恢复时间 + 负载影响