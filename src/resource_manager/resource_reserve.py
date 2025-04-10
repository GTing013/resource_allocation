from datetime import datetime, timedelta
import numpy as np

class ResourceReserve:
    def __init__(self):
        self.reserve_ratio = 0.2  # 基础预留比例
        self.peak_hours = [(9, 12), (14, 18)]  # 高峰时段
        self.usage_history = []
        self.forecast_window = 24  # 预测窗口（小时）
        
    def calculate_reserve(self, resource, current_usage):
        """计算资源预留量"""
        base_reserve = self._calculate_base_reserve(resource)
        dynamic_reserve = self._calculate_dynamic_reserve(current_usage)
        peak_reserve = self._calculate_peak_reserve()
        
        return max(base_reserve, dynamic_reserve, peak_reserve)
        
    def _calculate_base_reserve(self, resource):
        """计算基础预留量"""
        capacity = resource.get_capacity()
        return capacity * self.reserve_ratio
        
    def _calculate_dynamic_reserve(self, current_usage):
        """计算动态预留量"""
        if len(self.usage_history) < 24:
            return current_usage * 0.2
            
        # 使用历史数据预测
        usage_std = np.std(self.usage_history[-24:])
        usage_trend = np.mean(np.diff(self.usage_history[-6:]))
        
        return current_usage * (0.1 + 0.1 * usage_std + 0.1 * max(0, usage_trend))
        
    def _calculate_peak_reserve(self):
        """计算高峰期预留量"""
        current_hour = datetime.now().hour
        
        # 检查是否在高峰期
        in_peak = any(start <= current_hour < end for start, end in self.peak_hours)
        
        if in_peak:
            return self.usage_history[-24:].max() * 0.3 if self.usage_history else 0
        return 0