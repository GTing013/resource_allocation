import psutil
import logging
from datetime import datetime

class HealthChecker:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.thresholds = config['resources']
        
    def check_system_health(self):
        """检查系统健康状态"""
        try:
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health_status = {
                'timestamp': datetime.now(),
                'cpu': {
                    'usage': cpu_usage,
                    'status': 'healthy' if cpu_usage < self.thresholds['cpu_threshold'] else 'warning'
                },
                'memory': {
                    'usage': memory.percent,
                    'status': 'healthy' if memory.percent < self.thresholds['memory_threshold'] else 'warning'
                },
                'disk': {
                    'usage': disk.percent,
                    'status': 'healthy' if disk.percent < 85 else 'warning'
                }
            }
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"健康检查失败: {e}")
            return None