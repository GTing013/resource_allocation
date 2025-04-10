import logging
from datetime import datetime, timedelta
import numpy as np

class AutoScaler:
    def __init__(self, resource_limiter):
        self.resource_limiter = resource_limiter
        self.logger = logging.getLogger(__name__)
        self.scale_cooldown = 300  # 5分钟冷却时间
        self.last_scale = {}
        self.scale_history = {}
        
    def check_and_scale(self, workload_id, metrics):
        """检查并执行自动扩缩容"""
        if not self._can_scale(workload_id):
            return False
            
        scale_decision = self._make_scale_decision(metrics)
        if scale_decision == 0:
            return False
            
        return self._execute_scaling(workload_id, scale_decision)
        
    def _can_scale(self, workload_id):
        """检查是否可以进行扩缩容"""
        if workload_id not in self.last_scale:
            return True
            
        cooldown_passed = datetime.now() - self.last_scale[workload_id] > timedelta(seconds=self.scale_cooldown)
        return cooldown_passed
        
    def _make_scale_decision(self, metrics):
        """决定扩缩容行为"""
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)
        
        # 扩容条件
        if cpu_usage > 80 or memory_usage > 80:
            return 1
        # 缩容条件
        elif cpu_usage < 20 and memory_usage < 20:
            return -1
        return 0
        
    def _execute_scaling(self, workload_id, scale_direction):
        """执行扩缩容"""
        try:
            current_limits = self.resource_limiter.get_resource_limits(workload_id)
            new_limits = self._calculate_new_limits(current_limits, scale_direction)
            
            success = self.resource_limiter.apply_limits(workload_id, new_limits)
            if success:
                self.last_scale[workload_id] = datetime.now()
                self._record_scaling(workload_id, scale_direction, new_limits)
                
            return success
            
        except Exception as e:
            self.logger.error(f"执行扩缩容失败: {e}")
            return False
            
    def _calculate_new_limits(self, current_limits, scale_direction):
        """计算新的资源限制"""
        scale_factor = 1.5 if scale_direction > 0 else 0.75
        return {
            'cpu': current_limits['cpu'] * scale_factor,
            'memory': current_limits['memory'] * scale_factor
        }
        
    def _record_scaling(self, workload_id, direction, new_limits):
        """记录扩缩容历史"""
        if workload_id not in self.scale_history:
            self.scale_history[workload_id] = []
            
        self.scale_history[workload_id].append({
            'timestamp': datetime.now(),
            'direction': direction,
            'new_limits': new_limits
        })