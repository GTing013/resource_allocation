import numpy as np
from collections import defaultdict

class LoadBalancer:
    def __init__(self):
        self.resource_loads = defaultdict(float)
        self.history_window = 300  # 5分钟历史窗口
        self.load_history = defaultdict(list)
        self.overload_threshold = 0.8
        self.underload_threshold = 0.3
        
    def select_resource(self, resources, workload):
        """选择最优资源"""
        scores = self._calculate_scores(resources, workload)
        return max(resources, key=lambda r: scores[r])
        
    def _calculate_scores(self, resources, workload):
        """计算资源评分"""
        scores = {}
        for resource in resources:
            # 基础负载分数
            load_score = 1 - self.resource_loads[resource]
            
            # 历史表现分数
            history_score = self._calculate_history_score(resource)
            
            # 资源匹配度分数
            matching_score = self._calculate_matching_score(resource, workload)
            
            # 综合评分
            scores[resource] = 0.4 * load_score + 0.3 * history_score + 0.3 * matching_score
            
        return scores
        
    def _calculate_history_score(self, resource):
        """计算历史表现分数"""
        history = self.load_history[resource]
        if not history:
            return 0.5
            
        recent_loads = history[-self.history_window:]
        stability = 1 - np.std(recent_loads) if recent_loads else 1
        avg_load = np.mean(recent_loads) if recent_loads else 0
        
        return 0.6 * (1 - avg_load) + 0.4 * stability
        
    def _calculate_matching_score(self, resource, workload):
        """计算资源匹配度"""
        resource_capacity = resource.get_capacity()
        workload_demand = workload.get_resource_demand()
        
        # 计算资源匹配度
        matching_ratio = min(resource_capacity / workload_demand, 1.0)
        return matching_ratio