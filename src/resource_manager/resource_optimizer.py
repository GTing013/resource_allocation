class ResourceOptimizer:
    def __init__(self):
        self.min_utilization = 0.6
        self.max_utilization = 0.8
        
    def optimize_allocation(self, current_allocation, resource_usage):
        """优化资源分配"""
        optimized_allocation = current_allocation.copy()
        
        for resource_id, usage in resource_usage.items():
            if usage < self.min_utilization:
                # 减少资源分配
                optimized_allocation[resource_id] *= 0.8
            elif usage > self.max_utilization:
                # 增加资源分配
                optimized_allocation[resource_id] *= 1.2
                
        return optimized_allocation