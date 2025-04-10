import unittest
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.workload.workload_manager import WorkloadManager

class TestWorkloadManager(unittest.TestCase):
    def setUp(self):
        self.workload_manager = WorkloadManager()
        
    def test_create_workload(self):
        requirements = {'cpu': 2, 'memory': 4096}
        result = self.workload_manager.create_workload('test_workload_1', requirements)
        self.assertTrue(result)
        self.assertIn('test_workload_1', self.workload_manager.workloads)
        
    def test_delete_workload(self):
        requirements = {'cpu': 2, 'memory': 4096}
        self.workload_manager.create_workload('test_workload_2', requirements)
        result = self.workload_manager.delete_workload('test_workload_2')
        self.assertTrue(result)
        self.assertNotIn('test_workload_2', self.workload_manager.workloads)
        
    def test_update_workload_status(self):
        requirements = {'cpu': 2, 'memory': 4096}
        self.workload_manager.create_workload('test_workload_3', requirements)
        result = self.workload_manager.update_workload_status('test_workload_3', 'running')
        self.assertTrue(result)
        self.assertEqual(self.workload_manager.workloads['test_workload_3']['status'], 'running')
        
    def test_workload_priority(self):
        """测试工作负载优先级"""
        requirements = {'cpu': 2, 'memory': 4096}
        result = self.workload_manager.create_workload('high_priority', requirements, priority='high')
        self.assertTrue(result)
        self.assertEqual(self.workload_manager.workloads['high_priority']['priority'], 'high')
        
    def test_workload_metrics(self):
        """测试工作负载指标"""
        requirements = {'cpu': 2, 'memory': 4096}
        self.workload_manager.create_workload('test_metrics', requirements)
        metrics = {'cpu_usage': 50, 'memory_usage': 60}
        self.workload_manager.update_workload_metrics('test_metrics', metrics)
        self.assertEqual(
            self.workload_manager.workloads['test_metrics']['metrics']['cpu_usage'][-1],
            50
        )
        
    def test_workload_state_transition(self):
        """测试工作负载状态转换"""
        requirements = {'cpu': 2, 'memory': 4096}
        self.workload_manager.create_workload('test_state', requirements)
        
        # 测试状态转换
        states = ['pending', 'running', 'completed', 'failed']
        for state in states:
            result = self.workload_manager.update_workload_status('test_state', state)
            self.assertTrue(result)
            self.assertEqual(
                self.workload_manager.workloads['test_state']['status'],
                state
            )