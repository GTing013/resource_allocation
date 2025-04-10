import sys
import json
from datetime import datetime

# 添加项目根目录到 Python 路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 修改导入语句
from src.resource.allocator import ResourceAllocator
from src.analysis.performance_analyzer import PerformanceAnalyzer

def collect_baseline_data(duration=3600):  # 1小时测试
    """收集基准性能数据"""
    # 初始化资源分配器（使用默认配置）
    allocator = ResourceAllocator()
    analyzer = PerformanceAnalyzer()
    
    # 运行测试并收集数据
    test_data = allocator.run_test(duration)
    results = analyzer.analyze_performance(test_data)
    
    # 格式化基准数据
    baseline_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'metrics': {
            'latency': {
                'avg': results['latency']['avg_latency'],
                'std': results['latency']['p95_latency'] - results['latency']['avg_latency'],
                'min': min(test_data['latency_metrics']),
                'max': results['latency']['max_latency']
            },
            'throughput': {
                'avg': results['throughput']['avg_throughput'],
                'std': results['throughput']['stability'],
                'min': min(test_data['throughput_metrics']),
                'max': results['throughput']['peak_throughput']
            },
            'resource_utilization': {
                'avg': results['resource_efficiency']['resource_utilization'],
                'std': results['resource_efficiency']['cpu_efficiency'] - results['resource_efficiency']['memory_efficiency'],
                'min': min(test_data['metrics']['cpu_usage']),
                'max': max(test_data['metrics']['cpu_usage'])
            },
            'recovery_time': {
                'avg': results['recovery_time']['avg_recovery_time'],
                'std': results['recovery_time']['max_recovery_time'] - results['recovery_time']['avg_recovery_time'],
                'min': min([f['recovery_time'] - f['failure_time'] for f in test_data['failure_events']]),
                'max': results['recovery_time']['max_recovery_time']
            }
        }
    }
    
    # 保存基准数据
    save_path = '/Users/huanghaoting/resource_allocation/experiments/baseline/baseline_metrics.json'
    with open(save_path, 'w') as f:
        json.dump(baseline_data, f, indent=4)
    
    return baseline_data

if __name__ == "__main__":
    baseline_data = collect_baseline_data()
    print("基准数据收集完成，已保存到 baseline_metrics.json")