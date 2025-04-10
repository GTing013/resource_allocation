from datetime import datetime
import heapq
import logging

class WorkloadScheduler:
    def __init__(self, workload_manager):
        self.workload_manager = workload_manager
        self.priority_queue = []
        self.logger = logging.getLogger(__name__)
        
    def schedule_workload(self, workload_id):
        """调度工作负载"""
        workload = self.workload_manager.workloads.get(workload_id)
        if not workload:
            return False
            
        priority = self._calculate_priority(workload)
        heapq.heappush(self.priority_queue, (-priority, workload_id))
        return True
        
    def get_next_workload(self):
        """获取下一个要执行的工作负载"""
        if not self.priority_queue:
            return None
            
        _, workload_id = heapq.heappop(self.priority_queue)
        return workload_id
        
    def _calculate_priority(self, workload):
        """计算工作负载优先级"""
        base_priority = {
            'high': 100,
            'normal': 50,
            'low': 10
        }.get(workload.get('priority', 'normal'))
        
        # 等待时间权重
        wait_time = (datetime.now() - workload['created_at']).total_seconds()
        wait_factor = min(wait_time / 3600, 1)  # 最多等待1小时
        
        # 重试次数权重
        retry_penalty = workload.get('retries', 0) * 5
        
        return base_priority + (wait_factor * 20) - retry_penalty