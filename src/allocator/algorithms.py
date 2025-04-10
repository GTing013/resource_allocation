from .base_allocator import BaseAllocator
import numpy as np

class RoundRobinAllocator(BaseAllocator):
    def __init__(self):
        super().__init__()
        self.current_index = 0
    
    def allocate(self, workload_id, resource_request):
        available_resources = list(self.resources.keys())
        if not available_resources:
            return None
            
        resource = available_resources[self.current_index % len(available_resources)]
        self.current_index += 1
        self.current_allocation[workload_id] = resource
        return resource

class PriorityBasedAllocator(BaseAllocator):
    def __init__(self):
        super().__init__()
        self.priorities = {}
    
    def allocate(self, workload_id, resource_request):
        if not self.resources:
            return None
            
        # 根据优先级分配资源
        priority = self.priorities.get(workload_id, 0)
        available_resources = sorted(
            self.resources.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for resource_id, capacity in available_resources:
            if capacity >= resource_request:
                self.current_allocation[workload_id] = resource_id
                return resource_id
        return None

class LoadBasedAllocator(BaseAllocator):
    def __init__(self):
        super().__init__()
        self.load_threshold = 0.8  # 负载阈值
        self.buffer_ratio = 0.2    # 资源缓冲比例
        
    def allocate(self, workload_id, resource_request):
        # 添加预测负载的逻辑
        predicted_load = self._predict_load(workload_id)
        
        # 根据负载预测进行资源预分配
        if predicted_load > self.load_threshold:
            resource_request *= (1 + self.buffer_ratio)
            
        return super().allocate(workload_id, resource_request)