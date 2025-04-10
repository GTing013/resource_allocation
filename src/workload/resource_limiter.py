import psutil
import docker
import logging

class ResourceLimiter:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.logger = logging.getLogger(__name__)
        
    def apply_limits(self, workload_id, limits):
        """应用资源限制"""
        try:
            container = self.docker_client.containers.get(workload_id)
            
            update_config = {
                'cpu_period': 100000,
                'cpu_quota': int(limits['cpu'] * 100000),
                'memory': limits['memory'] * 1024 * 1024,  # 转换为字节
                'memory_swap': -1  # 禁用交换
            }
            
            container.update(**update_config)
            self.logger.info(f"已为工作负载 {workload_id} 应用资源限制")
            return True
            
        except Exception as e:
            self.logger.error(f"应用资源限制失败: {e}")
            return False
            
    def get_resource_usage(self, workload_id):
        """获取资源使用情况"""
        try:
            container = self.docker_client.containers.get(workload_id)
            stats = container.stats(stream=False)
            
            return {
                'cpu_usage': stats['cpu_stats']['cpu_usage']['total_usage'],
                'memory_usage': stats['memory_stats']['usage'],
                'network_io': stats['networks']
            }
            
        except Exception as e:
            self.logger.error(f"获取资源使用情况失败: {e}")
            return None