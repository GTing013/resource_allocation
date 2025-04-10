from ..workload.workload_manager import WorkloadManager
from ..storage.persistence_manager import PersistenceManager
from ..workload.priority_queue import WorkloadPriorityQueue
from ..resource.allocation_strategy import ResourceAllocationStrategy
from ..reporting.performance_reporter import PerformanceReporter
import logging

class SystemManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.workload_manager = WorkloadManager()
        self.persistence_manager = PersistenceManager(config['system']['db_path'])
        self.priority_queue = WorkloadPriorityQueue()
        self.allocation_strategy = ResourceAllocationStrategy()
        self.performance_reporter = PerformanceReporter(config['system']['report_dir'])
        self.health_checker = HealthChecker(config)
        self.alert_notifier = AlertNotifier(config)
        
    def submit_workload(self, workload_id, requirements, priority='normal'):
        """提交工作负载"""
        try:
            # 创建工作负载
            success = self.workload_manager.create_workload(
                workload_id, requirements, priority
            )
            if not success:
                return False
                
            # 持久化存储
            self.persistence_manager.save_workload(
                workload_id,
                self.workload_manager.workloads[workload_id]
            )
            
            # 加入优先级队列
            self.priority_queue.enqueue(workload_id, priority, requirements)
            
            return True
            
        except Exception as e:
            self.logger.error(f"提交工作负载失败: {e}")
            return False