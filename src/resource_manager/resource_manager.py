from datetime import datetime
import psutil

class ResourceManager:
    def __init__(self):
        self.resources = {}
        self.resource_states = {}
        self.capacity_thresholds = {
            'cpu': 0.8,
            'memory': 0.8,
            'disk': 0.9
        }
        
    def register_resource(self, resource_id, capacity):
        """注册新资源"""
        self.resources[resource_id] = capacity
        self.resource_states[resource_id] = {
            'status': 'available',
            'workloads': [],
            'last_updated': datetime.now()
        }
        
    def get_available_resources(self):
        """获取可用资源列表"""
        available = []
        for resource_id, state in self.resource_states.items():
            if (state['status'] == 'available' and 
                self._check_resource_health(resource_id)):
                available.append(resource_id)
        return available
        
    def allocate_resource(self, resource_id, workload):
        """分配资源"""
        if not self._check_capacity(resource_id, workload):
            return False
            
        try:
            state = self.resource_states[resource_id]
            state['workloads'].append(workload)
            state['last_updated'] = datetime.now()
            return True
        except Exception:
            return False
            
    def _check_resource_health(self, resource_id):
        """检查资源健康状态"""
        try:
            # 检查系统资源使用情况
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            
            return (cpu_usage < self.capacity_thresholds['cpu'] * 100 and
                   memory_usage < self.capacity_thresholds['memory'] * 100 and
                   disk_usage < self.capacity_thresholds['disk'] * 100)
        except:
            return False
            
    def _check_capacity(self, resource_id, workload):
        """检查资源容量"""
        try:
            capacity = self.resources[resource_id]
            required = workload.get_resource_requirements()
            
            return all(capacity[k] >= v for k, v in required.items())
        except:
            return False