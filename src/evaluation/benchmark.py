import numpy as np
import pandas as pd
from datetime import datetime

class Benchmark:
    def __init__(self):
        self.baseline_results = {}
        self.ml_results = {}
        self.metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        
    def run_baseline_tests(self, workload_generator, duration=3600, interval=60):
        """运行基准算法测试"""
        algorithms = ['round_robin', 'priority_based', 'load_based']
        results = {
            'latency': {},
            'throughput': {},
            'resource_utilization': {},
            'recovery_time': {}
        }
        
        for algo in algorithms:
            print(f"测试算法: {algo}")
            algo_results = self._run_single_test(algo, workload_generator, duration, interval)
            for metric in results:
                results[metric][algo] = algo_results[metric]
        
        return results  # 确保返回结果
    
    def run_ml_tests(self, workload_generator, duration=3600, interval=60):
        """运行机器学习算法测试"""
        results = {
            'latency': {},
            'throughput': {},
            'resource_utilization': {},
            'recovery_time': {}
        }
        
        algo_results = self._run_single_test('ml_allocator', workload_generator, duration, interval)
        for metric in results:
            results[metric]['ml_allocator'] = algo_results[metric]
        
        return results  # 确保返回结果
        
    def _run_single_test(self, algorithm, workload_generator, duration, interval):
        """运行单个算法测试"""
        results = {metric: [] for metric in self.metrics}
        
        # 生成工作负载
        workload = workload_generator.generate_workload(duration, interval)
        
        # 记录测试结果
        for metric in self.metrics:
            results[metric] = self._collect_metric(metric, algorithm, workload)
            
        return results
        
    def compare_results(self):
        """比较不同算法的性能"""
        comparison = {}
        
        # 合并所有结果
        all_results = {**self.baseline_results, **self.ml_results}
        
        # 计算每个指标的统计数据
        for metric in self.metrics:
            comparison[metric] = {
                algo: {
                    'mean': np.mean(results[metric]),
                    'std': np.std(results[metric]),
                    'min': np.min(results[metric]),
                    'max': np.max(results[metric])
                }
                for algo, results in all_results.items()
            }
            
        return pd.DataFrame(comparison)
    
    def _collect_metric(self, metric, algorithm, workload):
        """收集特定指标的测试数据"""
        timestamps, loads = workload
        metric_values = []
        
        if metric == 'latency':
            # 模拟延迟数据收集
            metric_values = self._simulate_latency(algorithm, loads)
        elif metric == 'throughput':
            # 模拟吞吐量数据收集
            metric_values = self._simulate_throughput(algorithm, loads)
        elif metric == 'resource_utilization':
            # 模拟资源利用率数据收集
            metric_values = self._simulate_resource_utilization(algorithm, loads)
        elif metric == 'recovery_time':
            # 模拟恢复时间数据收集
            metric_values = self._simulate_recovery_time(algorithm, loads)
            
        return metric_values
        
    def _simulate_latency(self, algorithm, loads):
        """模拟延迟数据"""
        base_latency = {
            'round_robin': 100,  # 基准延迟（毫秒）
            'priority_based': 80,
            'load_based': 90,
            'ml_allocator': 70
        }
        
        # 根据负载调整延迟
        return [base_latency[algorithm] * (1 + load) for load in loads]
        
    def _simulate_throughput(self, algorithm, loads):
        """模拟吞吐量数据"""
        base_throughput = {
            'round_robin': 1000,  # 基准吞吐量（请求/秒）
            'priority_based': 1200,
            'load_based': 1100,
            'ml_allocator': 1300
        }
        
        # 根据负载调整吞吐量
        return [base_throughput[algorithm] * (1 - 0.5 * load) for load in loads]
        
    def _simulate_resource_utilization(self, algorithm, loads):
        """模拟资源利用率数据"""
        efficiency = {
            'round_robin': 0.7,  # 基准效率
            'priority_based': 0.8,
            'load_based': 0.75,
            'ml_allocator': 0.85
        }
        
        # 根据负载计算资源利用率
        return [min(1.0, load * efficiency[algorithm]) for load in loads]
        
    def _simulate_recovery_time(self, algorithm, loads):
        """模拟故障恢复时间数据"""
        base_recovery = {
            'round_robin': 30,  # 基准恢复时间（秒）
            'priority_based': 25,
            'load_based': 28,
            'ml_allocator': 20
        }
        
        # 根据负载调整恢复时间
        return [base_recovery[algorithm] * (1 + 0.3 * load) for load in loads]
    
    def save_results(self, output_dir):
        """保存测试结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/benchmark_results_{timestamp}.csv"
        
        results_df = self.compare_results()
        results_df.to_csv(filename)
        return filename