from datetime import datetime
import json
import logging
from typing import Dict, Optional

class WorkloadManager:
    def __init__(self):
        self.workloads = {}
        self.workload_states = {}
        self.logger = logging.getLogger(__name__)
        
    def create_workload(self, workload_id, requirements, priority='normal'):
        """创建新工作负载"""
        try:
            if workload_id in self.workloads:
                self.logger.warning(f"工作负载 {workload_id} 已存在")
                return False
                
            self.workloads[workload_id] = {
                'id': workload_id,
                'requirements': requirements,
                'created_at': datetime.now(),
                'status': 'pending',
                'retries': 0,
                'priority': priority,
                'metrics': {
                    'cpu_usage': [],
                    'memory_usage': [],
                    'execution_time': 0
                }
            }
            self.logger.info(f"创建工作负载 {workload_id}, 优先级: {priority}")
            return True
        except Exception as e:
            self.logger.error(f"创建工作负载失败: {e}")
            return False
            
    def delete_workload(self, workload_id):
        """删除工作负载"""
        try:
            if workload_id in self.workloads:
                del self.workloads[workload_id]
                if workload_id in self.workload_states:
                    del self.workload_states[workload_id]
                self.logger.info(f"删除工作负载 {workload_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"删除工作负载失败: {e}")
            return False
            
    def get_workload_requirements(self, workload_id) -> Optional[Dict]:
        """获取工作负载资源需求"""
        try:
            workload = self.workloads.get(workload_id)
            if workload:
                return workload.get('requirements')
            return None
        except Exception as e:
            self.logger.error(f"获取工作负载需求失败: {e}")
            return None
            
    def update_workload_status(self, workload_id, status, message=None):
        """更新工作负载状态"""
        try:
            if workload_id in self.workloads:
                self.workloads[workload_id]['status'] = status
                self.workload_states[workload_id] = {
                    'state': status,
                    'message': message,
                    'updated_at': datetime.now()
                }
                self.logger.info(f"工作负载 {workload_id} 状态更新为 {status}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"更新工作负载状态失败: {e}")
            return False
            
    def increment_retry_count(self, workload_id):
        """增加重试次数"""
        try:
            if workload_id in self.workloads:
                self.workloads[workload_id]['retries'] += 1
                return self.workloads[workload_id]['retries']
            return 0
        except Exception as e:
            self.logger.error(f"增加重试次数失败: {e}")
            return 0
        
    def get_workload_state(self, workload_id):
        """获取工作负载状态"""
        return self.workload_states.get(workload_id, {})
        
    def update_workload_state(self, workload_id, state):
        """更新工作负载状态"""
        if workload_id in self.workloads:
            self.workload_states[workload_id] = {
                'state': state,
                'updated_at': datetime.now()
            }
            return True
        return False
        
    def save_workload_snapshot(self, workload_id):
        """保存工作负载快照"""
        if workload_id not in self.workloads:
            return None
            
        snapshot = {
            'workload': self.workloads[workload_id],
            'state': self.workload_states.get(workload_id, {}),
            'timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(snapshot)
        
    def restore_workload(self, snapshot):
        """从快照恢复工作负载"""
        try:
            data = json.loads(snapshot)
            workload = data['workload']
            state = data['state']
            
            self.workloads[workload['id']] = workload
            if state:
                self.workload_states[workload['id']] = state
                
            return True
        except:
            return False
        
    def update_workload_metrics(self, workload_id, metrics):
        """更新工作负载指标"""
        try:
            if workload_id not in self.workloads:
                self.logger.warning(f"工作负载 {workload_id} 不存在")
                return False
                
            if 'metrics' not in self.workloads[workload_id]:
                self.workloads[workload_id]['metrics'] = {
                    'cpu_usage': [],
                    'memory_usage': []
                }
                
            # 更新指标
            self.workloads[workload_id]['metrics']['cpu_usage'].append(metrics['cpu_usage'])
            self.workloads[workload_id]['metrics']['memory_usage'].append(metrics['memory_usage'])
            
            # 限制历史数据点数量
            max_points = 100
            for metric_type in ['cpu_usage', 'memory_usage']:
                if len(self.workloads[workload_id]['metrics'][metric_type]) > max_points:
                    self.workloads[workload_id]['metrics'][metric_type] = \
                        self.workloads[workload_id]['metrics'][metric_type][-max_points:]
                        
            return True
            
        except Exception as e:
            self.logger.error(f"更新工作负载指标失败: {e}")
            return False
            
    def get_workload_statistics(self, workload_id):
        """获取工作负载统计信息"""
        try:
            workload = self.workloads.get(workload_id)
            if not workload:
                return None
                
            metrics = workload['metrics']
            cpu_usage = metrics['cpu_usage']
            memory_usage = metrics['memory_usage']
            
            return {
                'cpu_stats': {
                    'avg': sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
                    'max': max(cpu_usage) if cpu_usage else 0,
                    'min': min(cpu_usage) if cpu_usage else 0
                },
                'memory_stats': {
                    'avg': sum(memory_usage) / len(memory_usage) if memory_usage else 0,
                    'max': max(memory_usage) if memory_usage else 0,
                    'min': min(memory_usage) if memory_usage else 0
                },
                'execution_time': metrics['execution_time'],
                'status': workload['status'],
                'retries': workload['retries']
            }
        except Exception as e:
            self.logger.error(f"获取工作负载统计信息失败: {e}")
            return None
            
    def get_all_active_workloads(self):
        """获取所有活跃的工作负载"""
        return {
            wid: workload for wid, workload in self.workloads.items()
            if workload['status'] in ['pending', 'running']
        }
        
    def cleanup_old_metrics(self, workload_id, max_age_hours=24):
        """清理旧的指标数据"""
        try:
            workload = self.workloads.get(workload_id)
            if not workload:
                return False
                
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=max_age_hours)
            
            # 清理超过指定时间的指标数据
            metrics = workload['metrics']
            for metric_type in ['cpu_usage', 'memory_usage']:
                metrics[metric_type] = [
                    m for m in metrics[metric_type]
                    if m['timestamp'] > cutoff_time
                ]
                
            return True
        except Exception as e:
            self.logger.error(f"清理旧指标数据失败: {e}")
            return False