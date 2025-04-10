import logging
from typing import Dict, List

class ResourceAllocationStrategy:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allocation_policies = {
            'high': self._allocate_high_priority,
            'normal': self._allocate_normal_priority,
            'low': self._allocate_low_priority
        }
        
    def allocate_resources(self, workload, available_resources):
        """分配资源"""
        try:
            priority = workload.get('priority', 'normal')
            allocator = self.allocation_policies.get(priority, self._allocate_normal_priority)
            return allocator(workload, available_resources)
        except Exception as e:
            self.logger.error(f"资源分配失败: {e}")
            return None
            
    def _allocate_high_priority(self, workload, resources):
        """高优先级资源分配策略"""
        required = workload['requirements']
        # 优先选择性能最好的资源
        best_resources = self._select_best_performing_resources(resources, required)
        return best_resources
        
    def _allocate_normal_priority(self, workload, resources):
        """普通优先级资源分配策略"""
        required = workload['requirements']
        # 选择满足要求且负载较低的资源
        suitable_resources = self._select_suitable_resources(resources, required)
        return suitable_resources
        
    def _allocate_low_priority(self, workload, resources):
        """低优先级资源分配策略"""
        required = workload['requirements']
        # 选择最经济的资源配置
        economic_resources = self._select_economic_resources(resources, required)
        return economic_resources