import unittest
import os
import tempfile
from src.system.system_manager import SystemManager
from src.config.config_manager import ConfigManager

class TestSystemIntegration(unittest.TestCase):
    def setUp(self):
        # 创建临时配置
        self.test_config = {
            'db_path': os.path.join(tempfile.gettempdir(), 'test.db'),
            'report_dir': os.path.join(tempfile.gettempdir(), 'reports'),
            'logging': {
                'directory': os.path.join(tempfile.gettempdir(), 'logs')
            }
        }
        
        # 初始化系统
        self.system = SystemManager(self.test_config)
        
    def test_workload_lifecycle(self):
        """测试工作负载生命周期"""
        # 创建工作负载
        workload_id = 'test_workload'
        requirements = {'cpu': 2, 'memory': 4096}
        
        # 提交工作负载
        success = self.system.submit_workload(workload_id, requirements, 'high')
        self.assertTrue(success)
        
        # 验证工作负载状态
        workload = self.system.workload_manager.workloads.get(workload_id)
        self.assertIsNotNone(workload)
        self.assertEqual(workload['status'], 'pending')
        
        # 更新指标
        metrics = {'cpu_usage': 50, 'memory_usage': 2048}
        success = self.system.workload_manager.update_workload_metrics(
            workload_id, metrics
        )
        self.assertTrue(success)
        
        # 生成性能报告
        success = self.system.performance_reporter.generate_report(
            workload_id,
            workload,
            metrics
        )
        self.assertTrue(success)