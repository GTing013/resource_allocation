from abc import ABC, abstractmethod

class BaseAllocator(ABC):
    def __init__(self):
        self.resources = {}
        self.current_allocation = {}
    
    @abstractmethod
    def allocate(self, workload_id, resource_request):
        """分配资源"""
        pass
    
    @abstractmethod
    def deallocate(self, workload_id):
        """释放资源"""
        pass
    
    def get_utilization(self):
        """获取资源利用率"""
        if not self.resources:
            return 0
        return sum(self.current_allocation.values()) / sum(self.resources.values())