import numpy as np
from collections import defaultdict

class AllocationOptimizer:
    def __init__(self, config):
        self.config = config
        self.history = defaultdict(list)
        self.optimization_window = config.get('optimization_window', 300)  # 5分钟
        
    def optimize_allocation(self, workload_data, current_allocation):
        """优化资源分配"""
        # 分析历史性能数据
        performance_trends = self._analyze_performance_trends(workload_data)
        
        # 预测资源需求
        predicted_demands = self._predict_resource_demands(performance_trends)
        
        # 计算最优分配
        optimal_allocation = self._calculate_optimal_allocation(
            predicted_demands,
            current_allocation
        )
        
        return optimal_allocation
        
    def _analyze_performance_trends(self, workload_data):
        """分析性能趋势"""
        trends = {}
        metrics = ['cpu_usage', 'memory_usage', 'throughput']
        
        for metric in metrics:
            if metric in workload_data:
                values = workload_data[metric][-self.optimization_window:]
                trends[metric] = {
                    'mean': np.mean(values),
                    'trend': np.polyfit(range(len(values)), values, 1)[0],
                    'volatility': np.std(values)
                }
                
        return trends
        
    def _predict_resource_demands(self, trends):
        """预测资源需求"""
        predictions = {}
        
        for metric, data in trends.items():
            # 基于趋势的预测
            base_prediction = data['mean'] + (data['trend'] * 10)  # 预测未来10个时间单位
            
            # 添加波动性缓冲
            buffer = data['volatility'] * 1.5
            
            predictions[metric] = base_prediction + buffer
            
        return predictions
        
    def _calculate_optimal_allocation(self, predicted_demands, current_allocation):
        """计算最优分配"""
        optimal = {}
        
        for resource, demand in predicted_demands.items():
            current = current_allocation.get(resource, 0)
            
            # 计算调整幅度
            adjustment = self._calculate_adjustment(
                current,
                demand,
                resource
            )
            
            optimal[resource] = current + adjustment
            
        return optimal
        
    def _calculate_adjustment(self, current, target, resource_type):
        """计算资源调整量"""
        # 获取资源特定的配置
        config = self.config.get(resource_type, {})
        min_adjustment = config.get('min_adjustment', 0.1)
        max_adjustment = config.get('max_adjustment', 0.5)
        
        # 计算理想调整量
        raw_adjustment = target - current
        
        # 应用调整限制
        if abs(raw_adjustment) < min_adjustment:
            return 0
            
        adjustment = np.clip(
            raw_adjustment,
            -current * max_adjustment,
            current * max_adjustment
        )
        
        return adjustment