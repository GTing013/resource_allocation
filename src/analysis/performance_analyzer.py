import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {
            'latency': self._analyze_latency,
            'throughput': self._analyze_throughput,
            'recovery_time': self._analyze_recovery_time,
            'resource_efficiency': self._analyze_resource_efficiency
        }
        
    def analyze_performance(self, workload_data, historical_data=None):
        """分析系统性能"""
        analysis_results = {}
        
        for metric, analyzer in self.metrics.items():
            analysis_results[metric] = analyzer(workload_data)
            
        # 与历史数据比较
        if historical_data:
            analysis_results['comparison'] = self._compare_with_historical(
                analysis_results, historical_data
            )
            
        # 计算综合评分
        analysis_results['overall_score'] = self._calculate_overall_score(analysis_results)
        
        return analysis_results
        
    def _analyze_latency(self, data):
        """分析延迟指标"""
        latency_data = data.get('latency_metrics', [])
        if not latency_data:
            return None
            
        return {
            'avg_latency': np.mean(latency_data),
            'p95_latency': np.percentile(latency_data, 95),
            'p99_latency': np.percentile(latency_data, 99),
            'max_latency': np.max(latency_data)
        }
        
    def _analyze_throughput(self, data):
        """分析吞吐量"""
        throughput_data = data.get('throughput_metrics', [])
        if not throughput_data:
            return None
            
        return {
            'avg_throughput': np.mean(throughput_data),
            'peak_throughput': np.max(throughput_data),
            'stability': np.std(throughput_data)
        }
        
    def _analyze_recovery_time(self, data):
        """分析故障恢复时间"""
        failures = data.get('failure_events', [])
        if not failures:
            return None
            
        recovery_times = []
        for failure in failures:
            recovery_time = failure['recovery_time'] - failure['failure_time']
            recovery_times.append(recovery_time.total_seconds())
            
        return {
            'avg_recovery_time': np.mean(recovery_times),
            'max_recovery_time': np.max(recovery_times),
            'recovery_success_rate': len([t for t in recovery_times if t < 300]) / len(recovery_times)
        }
        
    def _analyze_resource_efficiency(self, data):
        """分析资源使用效率"""
        cpu_usage = data.get('metrics', {}).get('cpu_usage', [])
        memory_usage = data.get('metrics', {}).get('memory_usage', [])
        
        if not cpu_usage or not memory_usage:
            return None
            
        return {
            'cpu_efficiency': self._calculate_resource_efficiency(cpu_usage),
            'memory_efficiency': self._calculate_resource_efficiency(memory_usage),
            'resource_utilization': (np.mean(cpu_usage) + np.mean(memory_usage)) / 2
        }
        
    def _calculate_resource_efficiency(self, usage_data):
        """计算资源效率得分"""
        mean_usage = np.mean(usage_data)
        std_usage = np.std(usage_data)
        
        # 理想使用率在60-80%之间
        if 60 <= mean_usage <= 80:
            base_score = 100
        else:
            base_score = 100 - abs(70 - mean_usage)
            
        # 稳定性影响
        stability_score = 100 - (std_usage * 2)
        
        return (base_score + stability_score) / 2
        
    def _compare_with_historical(self, current_results, historical_data):
        """与历史数据比较"""
        comparison = {}
        
        for metric in self.metrics:
            if metric in current_results and metric in historical_data:
                current = current_results[metric]
                historical = historical_data[metric]
                
                if current and historical:
                    comparison[metric] = {
                        'improvement': (current['avg_' + metric] - historical['avg_' + metric]) / historical['avg_' + metric] * 100,
                        'trend': 'improved' if current['avg_' + metric] > historical['avg_' + metric] else 'degraded'
                    }
                    
        return comparison
        
    def _calculate_overall_score(self, results):
        """计算综合性能得分"""
        weights = {
            'latency': 0.3,
            'throughput': 0.3,
            'recovery_time': 0.2,
            'resource_efficiency': 0.2
        }
        
        score = 0
        valid_weights_sum = 0
        
        for metric, weight in weights.items():
            if results.get(metric):
                metric_score = self._normalize_metric_score(results[metric])
                score += metric_score * weight
                valid_weights_sum += weight
                
        return score / valid_weights_sum if valid_weights_sum > 0 else 0
        
    def _normalize_metric_score(self, metric_data):
        """标准化指标得分"""
        if isinstance(metric_data, dict):
            # 根据不同指标类型计算得分
            if 'avg_latency' in metric_data:
                return 100 - min(metric_data['avg_latency'] / 1000, 100)
            elif 'avg_throughput' in metric_data:
                return min(metric_data['avg_throughput'] / 1000, 100)
            elif 'resource_utilization' in metric_data:
                return metric_data['resource_utilization']
        return 0


if __name__ == "__main__":
    # 创建测试数据
    test_data = {
        'latency_metrics': [100, 120, 95, 105, 110],
        'throughput_metrics': [800, 850, 900, 750, 820],
        'failure_events': [
            {
                'failure_time': datetime.now() - timedelta(minutes=30),
                'recovery_time': datetime.now() - timedelta(minutes=25)
            }
        ],
        'metrics': {
            'cpu_usage': [65, 70, 75, 68, 72],
            'memory_usage': [70, 75, 72, 68, 71]
        }
    }
    
    # 创建分析器实例
    analyzer = PerformanceAnalyzer()
    
    # 运行分析
    results = analyzer.analyze_performance(test_data)
    
    # 打印结果
    print("\n性能分析结果:")
    print("=" * 50)
    for metric, data in results.items():
        print(f"\n{metric}:")
        print("-" * 30)
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(value)


import numpy as np

class PerformanceAnalyzer:
    def analyze_performance(self, test_data):
        """分析性能数据"""
        return {
            'latency': {
                'avg_latency': np.mean(test_data['latency_metrics']),
                'p95_latency': np.percentile(test_data['latency_metrics'], 95),
                'max_latency': max(test_data['latency_metrics'])
            },
            'throughput': {
                'avg_throughput': np.mean(test_data['throughput_metrics']),
                'peak_throughput': max(test_data['throughput_metrics']),
                'stability': np.std(test_data['throughput_metrics'])
            },
            'resource_efficiency': {
                'resource_utilization': np.mean(test_data['metrics']['cpu_usage']),
                'cpu_efficiency': np.mean(test_data['metrics']['cpu_usage']),
                'memory_efficiency': np.mean(test_data['metrics']['memory_usage'])
            },
            'recovery_time': {
                'avg_recovery_time': np.mean([f['recovery_time'] - f['failure_time'] 
                                           for f in test_data['failure_events']]) if test_data['failure_events'] else 0,
                'max_recovery_time': max([f['recovery_time'] - f['failure_time'] 
                                       for f in test_data['failure_events']]) if test_data['failure_events'] else 0
            }
        }