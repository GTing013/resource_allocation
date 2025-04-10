import heapq
from datetime import datetime
import logging

class WorkloadPriorityQueue:
    def __init__(self):
        self.queue = []
        self.priority_levels = {
            'high': 3,
            'normal': 2,
            'low': 1
        }
        self.logger = logging.getLogger(__name__)
        
    def enqueue(self, workload_id, priority, requirements):
        """将工作负载加入队列"""
        try:
            priority_value = self.priority_levels.get(priority, 1)
            timestamp = datetime.now().timestamp()
            
            # 使用负优先级确保高优先级在前
            heapq.heappush(self.queue, (-priority_value, timestamp, workload_id, requirements))
            return True
        except Exception as e:
            self.logger.error(f"加入队列失败: {e}")
            return False
            
    def dequeue(self):
        """获取最高优先级的工作负载"""
        if not self.queue:
            return None
        try:
            _, _, workload_id, requirements = heapq.heappop(self.queue)
            return workload_id, requirements
        except Exception as e:
            self.logger.error(f"出队列失败: {e}")
            return None