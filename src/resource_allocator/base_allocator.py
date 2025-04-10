from abc import ABC, abstractmethod

class BaseResourceAllocator(ABC):
    def __init__(self):
        self.resources = {}
        self.workloads = {}
    
    @abstractmethod
    def allocate(self, workload, available_resources):
        """分配资源的抽象方法"""
        pass
    
    @abstractmethod
    def deallocate(self, workload_id):
        """释放资源的抽象方法"""
        pass
    
    def get_metrics(self):
        """获取性能指标"""
        return {
            'utilization': self.calculate_utilization(),
            'latency': self.measure_latency(),
            'throughput': self.measure_throughput()
        }