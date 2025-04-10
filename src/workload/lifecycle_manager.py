from datetime import datetime
import logging
from .workload_scheduler import WorkloadScheduler
from .resource_limiter import ResourceLimiter
from .workload_monitor import WorkloadMonitor

class WorkloadLifecycleManager:
    def __init__(self, workload_manager):
        self.workload_manager = workload_manager
        self.scheduler = WorkloadScheduler(workload_manager)
        self.resource_limiter = ResourceLimiter()
        self.monitor = WorkloadMonitor(workload_manager)
        self.logger = logging.getLogger(__name__)
        
    def submit_workload(self, workload_id, requirements, priority='normal'):
        """提交工作负载"""
        try:
            # 创建工作负载
            success = self.workload_manager.create_workload(
                workload_id, requirements, priority
            )
            if not success:
                return False
                
            # 调度工作负载
            self.scheduler.schedule_workload(workload_id)
            
            # 启动监控
            self.monitor.start_monitoring(workload_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"提交工作负载失败: {e}")
            return False
            
    def start_workload(self, workload_id):
        """启动工作负载"""
        try:
            # 获取工作负载配置
            workload = self.workload_manager.workloads.get(workload_id)
            if not workload:
                return False
                
            # 应用资源限制
            limits = workload['requirements']
            self.resource_limiter.apply_limits(workload_id, limits)
            
            # 更新状态
            self.workload_manager.update_workload_status(workload_id, 'running')
            
            return True
            
        except Exception as e:
            self.logger.error(f"启动工作负载失败: {e}")
            return False
            
    def stop_workload(self, workload_id):
        """停止工作负载"""
        try:
            # 更新状态
            self.workload_manager.update_workload_status(workload_id, 'stopping')
            
            # 释放资源
            self.resource_limiter.release_resources(workload_id)
            
            # 清理工作负载
            self.workload_manager.delete_workload(workload_id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"停止工作负载失败: {e}")
            return False